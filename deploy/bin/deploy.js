#!/usr/bin/env node
import cdk  from 'aws-cdk-lib';
import { DynamoDBRagStack } from '../lib/ddb-rag.js';
import * as dotenv from 'dotenv' ;
dotenv.config()

console.log(process.env.CDK_DEFAULT_ACCOUNT,process.env.CDK_DEFAULT_REGION);
const app = new cdk.App();

new DynamoDBRagStack(app, 'DynamoDBRagDeployStack', {
  env: { account: process.env.CDK_DEFAULT_ACCOUNT, region: process.env.CDK_DEFAULT_REGION},
});
