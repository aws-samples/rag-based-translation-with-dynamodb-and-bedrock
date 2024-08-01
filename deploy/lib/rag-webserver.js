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
// import * as cdk from 'aws-cdk-lib';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as elbv2 from 'aws-cdk-lib/aws-elasticloadbalancingv2';
import * as iam from 'aws-cdk-lib/aws-iam';

dotenv.config();

import path from "path";
import { fileURLToPath } from "url";
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

import { join } from "path";
export class RagWebserverStack extends Stack {
    /**
     *
     * @param {Construct} scope
     * @param {string} id
     * @param {StackProps=} props
     */
    constructor(scope, id, props) {
      super(scope, id, props);

      // 创建 VPC
    const vpc = new ec2.Vpc(this, 'RagWebVPC', {
        maxAzs: 2,
        subnetConfiguration: [
          {
            cidrMask: 24,
            name: 'Public',
            subnetType: ec2.SubnetType.PUBLIC,
          },
          {
            cidrMask: 24,
            name: 'Private',
            subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS,
          },
        ],
      });
  
      // 创建 ALB 安全组
      const albSg = new ec2.SecurityGroup(this, 'AlbSecurityGroup', {
        vpc,
        allowAllOutbound: true,
        description: 'Security group for ALB',
      });
      albSg.addIngressRule(ec2.Peer.anyIpv4(), ec2.Port.tcp(80), 'Allow HTTP traffic');
  
      // 创建 EC2 安全组
      const ec2Sg = new ec2.SecurityGroup(this, 'Ec2SecurityGroup', {
        vpc,
        allowAllOutbound: true,
        description: 'Security group for EC2 instance',
      });
      ec2Sg.addIngressRule(albSg, ec2.Port.tcp(8501), 'Allow traffic from ALB');
  
      // 创建 ALB
      const alb = new elbv2.ApplicationLoadBalancer(this, 'TranslationALB', {
        vpc,
        internetFacing: true,
        securityGroup: albSg,
      });
  
      // 创建 ALB 监听器
      const listener = alb.addListener('TranslationListener', {
        port: 80,
        open: true,
      });
  
      // 创建 EC2 实例
      const ec2Instance = new ec2.Instance(this, 'TranslateWebServer', {
        vpc,
        vpcSubnets: { subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS },
        instanceType: ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.MICRO),
        machineImage: ec2.MachineImage.latestAmazonLinux2(),
        securityGroup: ec2Sg,
      });
  
      // 添加 EC2 实例到 ALB 目标组
      const targetGroup = listener.addTargets('EC2Target', {
        port: 8501,
        targets: [ec2Instance],
        healthCheck: {
          path: '/',
          port: '8501',
        },
      });
  
      // 输出 ALB DNS 名称
      new cdk.CfnOutput(this, 'AlbDnsName', {
        value: alb.loadBalancerDnsName,
        description: 'ALB DNS Name',
      });

    }

}