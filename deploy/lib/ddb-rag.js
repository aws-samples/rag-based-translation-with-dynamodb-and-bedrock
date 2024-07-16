// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import { Stack, Duration, CfnOutput, RemovalPolicy } from "aws-cdk-lib";
import { DockerImageFunction }  from 'aws-cdk-lib/aws-lambda';
import { DockerImageCode,Architecture } from 'aws-cdk-lib/aws-lambda';
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as iam from "aws-cdk-lib/aws-iam";
import * as ecr from 'aws-cdk-lib/aws-ecr';
import { VpcStack } from './vpc-stack.js';
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
export class DynamoDBRagStack extends Stack {
  /**
   *
   * @param {Construct} scope
   * @param {string} id
   * @param {StackProps=} props
   */
  constructor(scope, id, props) {
    super(scope, id, props);

    const region = props.env.region;
    const account_id = Stack.of(this).account;
    const aos_existing_endpoint = props.env.aos_existing_endpoint;

    const vpcStack = new VpcStack(this,'vpc-stack',{env:process.env});
    const vpc = vpcStack.vpc;
    const subnets = vpcStack.subnets;
    const securityGroups = vpcStack.securityGroups;
    
    const bucket = new s3.Bucket(this, 'DocUploadBucket', {
      removalPolicy: RemovalPolicy.DESTROY,
      bucketName:process.env.UPLOAD_BUCKET,
      cors:[{
        allowedMethods: [s3.HttpMethods.GET,s3.HttpMethods.POST,s3.HttpMethods.PUT],
        allowedOrigins: ['*'],
        allowedHeaders: ['*'],
      }]
    });

    const online_processor = new DockerImageFunction(this,
      "lambda_online_processor", {
      code: DockerImageCode.fromImageAsset(join(__dirname, "../../code/online_process")),
      timeout: Duration.minutes(15),
      memorySize: 1024,
      runtime: 'python3.9',
      functionName: 'translate_tool',
      vpc:vpc,
      vpcSubnets:subnets,
      securityGroups:securityGroups,
      architecture: Architecture.X86_64,
      environment: {
        user_dict_bucket:`${process.env.UPLOAD_BUCKET}`,
        user_dict_prefix:'translate'
      },
    });

    online_processor.addToRolePolicy(new iam.PolicyStatement({
      // principals: [new iam.AnyPrincipal()],
        actions: [ 
          "s3:List*",
          "s3:Put*",
          "s3:Get*",
          "bedrock:*",
          "dynamodb:GetItem"
          ],
        effect: iam.Effect.ALLOW,
        resources: ['*'],
        }))

    const connection = new glue.Connection(this, 'GlueJobConnection', {
      type:glue.ConnectionType.NETWORK,
      vpc:vpc,
      securityGroups:securityGroups,
      subnet:subnets[0],
    });

    const ingest_ddb_job = new glue.Job(this, 'ingest-knowledge-to-ddb',{
          executable: glue.JobExecutable.pythonShell({
          glueVersion: glue.GlueVersion.V1_0,
          pythonVersion: glue.PythonVersion.THREE_NINE,
          script: glue.Code.fromAsset(path.join(__dirname, '../../code/offline_process/ddb_write_job.py')),
        }),
        jobName:'ingest_knowledge2ddb',
        maxConcurrentRuns:100,
        maxRetries:0,
        connections:[connection],
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

      const rag_job = new glue.Job(this, 'rag-process',{
            executable: glue.JobExecutable.pythonShell({
            glueVersion: glue.GlueVersion.V1_0,
            pythonVersion: glue.PythonVersion.THREE_NINE,
            script: glue.Code.fromAsset(path.join(__dirname, '../../code/offline_process/rag_based_translate.py')),
          }),
          jobName:'rag_based_translate',
          maxConcurrentRuns:100,
          maxRetries:0,
          connections:[connection],
          maxCapacity:1,
          defaultArguments:{
              '--REGION':region,
              '--additional-python-modules': 'boto3>=1.28.52,botocore>=1.31.52',
              '--model_id': 'anthropic.claude-3-sonnet-20240229-v1:0',
              '--object_key': 'src_files/chat_text.json',
              '--bucket': '687752207838-24-04-10-02-26-15-aos-rag-bucket'
          }
      })
      rag_job.role.addToPrincipalPolicy(
        new iam.PolicyStatement({
              actions: [ 
                "sagemaker:InvokeEndpointAsync",
                "sagemaker:InvokeEndpoint",
                "s3:List*",
                "s3:Put*",
                "s3:Get*",
                "dynamodb:*",
                "bedrock:*",
                "lambda:InvokeFunction",
                ],
              effect: iam.Effect.ALLOW,
              resources: ['*'],
              })
      )

    // const rag_meta_en_table = new Table(this, "rag-meta-en-table", {
    //   partitionKey: {
    //     name: "term",
    //     type: AttributeType.STRING,
    //   },
    //   tableName:'rag_translate_en_table',
    //   removalPolicy: RemovalPolicy.DESTROY,
    //   billingMode: BillingMode.PAY_PER_REQUEST,
    // });

    // const rag_meta_chs_table = new Table(this, "rag-meta-chs-table", {
    //   partitionKey: {
    //     name: "term",
    //     type: AttributeType.STRING,
    //   },
    //   tableName:'rag_translate_chs_table',
    //   removalPolicy: RemovalPolicy.DESTROY,
    //   billingMode: BillingMode.PAY_PER_REQUEST,
    // });

    // rag_meta_en_table.grantReadWriteData(ingest_ddb_job);
    // rag_meta_chs_table.grantReadWriteData(ingest_ddb_job);
    // rag_meta_en_table.grantReadWriteData(rag_job);
    // rag_meta_chs_table.grantReadWriteData(rag_job);
    // rag_meta_en_table.grantReadWriteData(online_processor);
    // rag_meta_chs_table.grantReadWriteData(online_processor);

    new CfnOutput(this,'VPC',{value:vpc.vpcId});
    new CfnOutput(this,'region',{value:process.env.CDK_DEFAULT_REGION});
    new CfnOutput(this,'UPLOAD_BUCKET',{value:process.env.UPLOAD_BUCKET});
  }
}
