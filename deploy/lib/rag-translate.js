// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import { Stack, Duration, CfnOutput, RemovalPolicy } from "aws-cdk-lib";
import { DockerImageFunction }  from 'aws-cdk-lib/aws-lambda';
import { DockerImageCode,Architecture } from 'aws-cdk-lib/aws-lambda';
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as iam from "aws-cdk-lib/aws-iam";
import * as ecr from 'aws-cdk-lib/aws-ecr';
// import { VpcStack } from './translate-vpc.js';
import * as glue from  '@aws-cdk/aws-glue-alpha';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as s3n from 'aws-cdk-lib/aws-s3-notifications';
import * as dotenv from "dotenv";

import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
const { AttributeType, BillingMode, Table } = dynamodb;

dotenv.config();

import path from "path";
import { fileURLToPath } from "url";
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

import { join } from "path";
export class RagTranslateStack extends Stack {
    /**
     *
     * @param {Construct} scope
     * @param {string} id
     * @param {StackProps=} props
     */
    constructor(scope, id, props) {
      super(scope, id, props);

      

      // Create S3 Bucket to store Dictionary File
      const bucket = new s3.Bucket(this, 'DocUploadBucket', {
        removalPolicy: RemovalPolicy.DESTROY,
        bucketName:process.env.UPLOAD_BUCKET,
        cors:[{
          allowedMethods: [s3.HttpMethods.GET,s3.HttpMethods.POST,s3.HttpMethods.PUT],
          allowedOrigins: ['*'],
          allowedHeaders: ['*'],
        }]
      });

      // Create online translate lambda
      const online_processor = new DockerImageFunction(this,
        "lambda_online_processor", {
        code: DockerImageCode.fromImageAsset(join(__dirname, "../../code/online_process")),
        timeout: Duration.minutes(15),
        memorySize: 2048,
        runtime: 'python3.9',
        functionName: 'translate_tool',
        architecture: Architecture.X86_64,
        environment: {
          user_dict_bucket:`${process.env.UPLOAD_BUCKET}`,
          user_dict_prefix:'translate',
          bedrock_region:`us-west-2`
        },
      });

      const alias = new lambda.Alias(this, 'ProductionAlias', {
        aliasName: 'staging',
        version: online_processor.currentVersion,
      });
  
      online_processor.addToRolePolicy(new iam.PolicyStatement({
        // principals: [new iam.AnyPrincipal()],
          actions: [ 
            "s3:List*",
            "s3:Put*",
            "s3:Get*",
            "bedrock:*",
            "dynamodb:GetItem",
            "ssm:GetParameter"
            ],
          effect: iam.Effect.ALLOW,
          resources: ['*'],
          }))

          const ingest_ddb_job = new glue.Job(this, 'ingest-knowledge-to-ddb',{
            executable: glue.JobExecutable.pythonShell({
            glueVersion: glue.GlueVersion.V4_0,
            pythonVersion: glue.PythonVersion.THREE_NINE,
            script: glue.Code.fromAsset(path.join(__dirname, '../../code/offline_process/ddb_write_job.py')),
          }),
          jobName:'ingest_knowledge2ddb',
          maxConcurrentRuns:100,
          maxRetries:0,
          maxCapacity:1,
          defaultArguments:{
              '--additional-python-modules': 'boto3>=1.28.52,botocore>=1.31.52',
              '--dictionary_name': 'dictionary_1',
              '--bucket': process.env.UPLOAD_BUCKET,
              '--object_key': 'translate/dictionary_1/dictionary_1_part_a.json'
          }
      })
  
      ingest_ddb_job.role.addToPrincipalPolicy(
        new iam.PolicyStatement({
              actions: [ 
                "s3:List*",
                "s3:Put*",
                "s3:Get*",
                "dynamodb:*",
                ],
              effect: iam.Effect.ALLOW,
              resources: ['*'],
              })
      )

      const translation_meta_table = new Table(this, "translation-meta-table", {
        partitionKey: {
          name: "dict",
          type: AttributeType.STRING,
        },
        tableName: 'translate_meta',
        removalPolicy: RemovalPolicy.DESTROY,
        billingMode: BillingMode.PAY_PER_REQUEST,
      });

      // // Create VPC and Subnets
      // const vpcStack = new VpcStack(this,'vpc-stack',{env:process.env});
      // const vpc = vpcStack.vpc;
      // const subnets = vpcStack.subnets;

      new CfnOutput(this,'region',{value:process.env.CDK_DEFAULT_REGION});
      new CfnOutput(this,'UPLOAD_BUCKET',{value:process.env.UPLOAD_BUCKET});
    }

}