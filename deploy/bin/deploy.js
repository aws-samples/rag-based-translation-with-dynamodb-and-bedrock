#!/usr/bin/env node
import cdk  from 'aws-cdk-lib';
import {RagTranslateStack} from '../lib/rag-translate.js';
import {RagWebserverStack} from '../lib/rag-webserver.js';
import * as dotenv from 'dotenv' ;
dotenv.config()

console.log(process.env.CDK_DEFAULT_ACCOUNT,process.env.CDK_DEFAULT_REGION);
const app = new cdk.App();

// new DynamoDBRagStack(app, 'DynamoDBRagDeployStack', {
//   env: { account: process.env.CDK_DEFAULT_ACCOUNT, region: process.env.CDK_DEFAULT_REGION},
// });

new RagTranslateStack(app, 'RagTranslateStack', {
  env: { account: process.env.CDK_DEFAULT_ACCOUNT, region: process.env.CDK_DEFAULT_REGION},
});

new RagWebserverStack(app, 'RagWebserverStack', {
  env: { account: process.env.CDK_DEFAULT_ACCOUNT, region: process.env.CDK_DEFAULT_REGION},
});