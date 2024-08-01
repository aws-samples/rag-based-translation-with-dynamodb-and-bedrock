// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import { Stack, Duration, CfnOutput, RemovalPolicy } from "aws-cdk-lib";
import * as iam from "aws-cdk-lib/aws-iam";
import * as dotenv from "dotenv";
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as elbv2 from 'aws-cdk-lib/aws-elasticloadbalancingv2';
import * as targets from 'aws-cdk-lib/aws-elasticloadbalancingv2-targets';

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
  
      // 创建 IAM 角色
      const ec2Role = new iam.Role(this, 'EC2Role', {
        assumedBy: new iam.ServicePrincipal('ec2.amazonaws.com'),
      });

      // 添加所需的 IAM 权限
      ec2Role.addToPolicy(new iam.PolicyStatement({
        effect: iam.Effect.ALLOW,
        actions: [
          'ssm:GetParametersByPath',
          'ssm:PutParameter',
        ],
        resources: ['arn:aws:ssm:*:*:parameter/*'],
      }));

      ec2Role.addToPolicy(new iam.PolicyStatement({
        effect: iam.Effect.ALLOW,
        actions: [
          'comprehend:DetectDominantLanguage',
        ],
        resources: ['*'],
      }));

      ec2Role.addToPolicy(new iam.PolicyStatement({
        effect: iam.Effect.ALLOW,
        actions: [
          'dynamodb:ListTables',
          'dynamodb:GetItem',
          'dynamodb:PutItem',
          'dynamodb:DeleteItem',
        ],
        resources: ['arn:aws:dynamodb:*:*:table/*'],
      }));

      ec2Role.addToPolicy(new iam.PolicyStatement({
        effect: iam.Effect.ALLOW,
        actions: [
          'lambda:InvokeFunction',
        ],
        resources: ['arn:aws:lambda:*:*:function:*'],
      }));

      ec2Role.addToPolicy(new iam.PolicyStatement({
        effect: iam.Effect.ALLOW,
        actions: [
          's3:PutObject',
        ],
        resources: ['arn:aws:s3:::*/*'],
      }));

      ec2Role.addToPolicy(new iam.PolicyStatement({
        effect: iam.Effect.ALLOW,
        actions: [
          'glue:GetJobRun',
        ],
        resources: ['arn:aws:glue:*:*:job/*'],
      }));
  
      // 创建 EC2 实例
      const ec2Instance = new ec2.Instance(this, 'TranslateWebServer', {
        vpc,
        vpcSubnets: { subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS },
        instanceType: ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.LARGE),
        machineImage: ec2.MachineImage.latestAmazonLinux2023(),
        securityGroup: ec2Sg,
        role: ec2Role, 
      });
  
      const targetGroup = new elbv2.ApplicationTargetGroup(this, 'EC2TargetGroup', {
        vpc,
        port: 8501,
        protocol: elbv2.ApplicationProtocol.HTTP,
        targets: [new targets.InstanceTarget(ec2Instance)],
        healthCheck: {
          path: '/',
          port: '8501',
        },
      });

      // 创建 ALB 监听器并添加目标组
        const listener = alb.addListener('MyListener', {
        port: 80,
        open: true,
        defaultTargetGroups: [targetGroup],
      });
  
      // 输出 ALB DNS 名称
      new CfnOutput(this, 'AlbDnsName', {
        value: alb.loadBalancerDnsName,
        description: 'ALB DNS Name',
      });

    }

}