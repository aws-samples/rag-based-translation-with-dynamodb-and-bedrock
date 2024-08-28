#!/bin/bash

# Set environment variables (replace these with your actual values)
export AWS_REGION="your-region"
export UPLOAD_BUCKET="your-upload-bucket-name"
export VPC_ID="your-vpc-id"
export SUBNET_ID="your-subnet-id"
export SECURITY_GROUP_ID="your-security-group-id"
export LAMBDA_ROLE_NAME="lambda-segmentor-role"
export GLUE_INGEST_ROLE_NAME="glue-ingest-role"
export GLUE_RAG_ROLE_NAME="glue-rag-role"

ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# Create S3 Bucket
aws s3api create-bucket --bucket $UPLOAD_BUCKET --region $AWS_REGION

# Set CORS on S3 Bucket
aws s3api put-bucket-cors --bucket $UPLOAD_BUCKET --cors-configuration file://cors-config.json

# Upload Glue job scripts to S3
aws s3 cp ./code/offline_process/ddb_write_job.py s3://$UPLOAD_BUCKET/glue_scripts/ddb_write_job.py
aws s3 cp ./code/offline_process/rag_based_translate.py s3://$UPLOAD_BUCKET/glue_scripts/rag_based_translate.py

# Create IAM Roles
aws iam create-role --role-name $LAMBDA_ROLE_NAME --assume-role-policy-document '{"Version": "2012-10-17","Statement": [{ "Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, "Action": "sts:AssumeRole"}]}'
aws iam create-role --role-name $GLUE_INGEST_ROLE_NAME --assume-role-policy-document '{"Version": "2012-10-17","Statement": [{ "Effect": "Allow", "Principal": {"Service": "glue.amazonaws.com"}, "Action": "sts:AssumeRole"}]}'
aws iam create-role --role-name $GLUE_RAG_ROLE_NAME --assume-role-policy-document '{"Version": "2012-10-17","Statement": [{ "Effect": "Allow", "Principal": {"Service": "glue.amazonaws.com"}, "Action": "sts:AssumeRole"}]}'

# Create custom policies
aws iam create-policy --policy-name lambda-segmentor-policy --policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Action": [
            "s3:List*",
            "s3:Put*",
            "s3:Get*"
        ],
        "Resource": "*"
    }]
}'

aws iam create-policy --policy-name glue-ingest-policy --policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Action": [
            "s3:List*",
            "s3:Put*",
            "s3:Get*",
            "dynamodb:*"
        ],
        "Resource": "*"
    }]
}'

aws iam create-policy --policy-name glue-rag-policy --policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Action": [
            "sagemaker:InvokeEndpointAsync",
            "sagemaker:InvokeEndpoint",
            "s3:List*",
            "s3:Put*",
            "s3:Get*",
            "dynamodb:*",
            "bedrock:*",
            "lambda:InvokeFunction"
        ],
        "Resource": "*"
    }]
}'

# Attach policies to roles
aws iam attach-role-policy --role-name $LAMBDA_ROLE_NAME --policy-arn arn:aws:iam::$ACCOUNT_ID:policy/lambda-segmentor-policy
aws iam attach-role-policy --role-name $GLUE_INGEST_ROLE_NAME --policy-arn arn:aws:iam::$ACCOUNT_ID:policy/glue-ingest-policy
aws iam attach-role-policy --role-name $GLUE_RAG_ROLE_NAME --policy-arn arn:aws:iam::$ACCOUNT_ID:policy/glue-rag-policy

# Create Lambda function (simplified, doesn't include Docker image building)
aws lambda create-function \
    --function-name jieba_segmentor \
    --runtime python3.9 \
    --role arn:aws:iam::$ACCOUNT_ID:role/$LAMBDA_ROLE_NAME \
    --handler index.handler \
    --code S3Bucket=$UPLOAD_BUCKET,S3Key=lambda-code.zip \
    --timeout 900 \
    --memory-size 1024 \
    --vpc-config SubnetIds=$SUBNET_ID,SecurityGroupIds=$SECURITY_GROUP_ID \
    --environment "Variables={user_dict_bucket=$UPLOAD_BUCKET,user_dict_path=user_dict/user_dict.txt}"

# Create Glue Connection
aws glue create-connection --connection-input '{
    "Name": "GlueJobConnection",
    "ConnectionType": "NETWORK",
    "ConnectionProperties": {"JDBC_ENFORCE_SSL": "false"},
    "PhysicalConnectionRequirements": {
        "SubnetId": "'$SUBNET_ID'",
        "SecurityGroupIdList": ["'$SECURITY_GROUP_ID'"],
        "AvailabilityZone": "'$AWS_REGION'a"
    }
}'

# Create Glue Jobs
aws glue create-job \
    --name ingest_knowledge2ddb \
    --role arn:aws:iam::$ACCOUNT_ID:role/$GLUE_INGEST_ROLE_NAME \
    --command '{"Name": "pythonshell", "ScriptLocation": "s3://'$UPLOAD_BUCKET'/ddb_write_job.py"}' \
    --default-arguments '{
        "--dynamodb_table_name": "rag-translate-table",
        "--REGION": "'$AWS_REGION'",
        "--additional-python-modules": "boto3>=1.28.52,botocore>=1.31.52",
        "--bucket": "'$UPLOAD_BUCKET'",
        "--object_key": "kb/multilingual_terminology.json"
    }' \
    --max-capacity 1

aws glue create-job \
    --name rag_based_translate \
    --role arn:aws:iam::$ACCOUNT_ID:role/$GLUE_RAG_ROLE_NAME \
    --command '{"Name": "pythonshell", "ScriptLocation": "s3://'$UPLOAD_BUCKET'/rag_based_translate.py"}' \
    --default-arguments '{
        "--REGION": "'$AWS_REGION'",
        "--additional-python-modules": "boto3>=1.28.52,botocore>=1.31.52",
        "--model_id": "anthropic.claude-3-sonnet-20240229-v1:0",
        "--object_key": "src_files/chat_text.json",
        "--bucket": "'$UPLOAD_BUCKET'"
    }' \
    --max-capacity 1

# Create DynamoDB Tables
aws dynamodb create-table \
    --table-name rag_translate_en_table \
    --attribute-definitions AttributeName=term,AttributeType=S \
    --key-schema AttributeName=term,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST

aws dynamodb create-table \
    --table-name rag_translate_chs_table \
    --attribute-definitions AttributeName=term,AttributeType=S \
    --key-schema AttributeName=term,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST

echo "Script execution completed. Please check for any errors and adjust as needed."
