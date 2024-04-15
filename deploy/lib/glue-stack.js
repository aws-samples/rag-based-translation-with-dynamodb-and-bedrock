import * as glue from  '@aws-cdk/aws-glue-alpha';
import { NestedStack,Duration, CfnOutput }  from 'aws-cdk-lib';
import * as iam from "aws-cdk-lib/aws-iam";
import * as dotenv from "dotenv";
dotenv.config();
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export class GlueStack extends NestedStack {

    jobArn = '';
    jobName = '';
    ragJobName = '';
    /**
     *
     * @param {Construct} scope
     * @param {string} id
     * @param {StackProps=} props
     */
    constructor(scope, id, props) {
      super(scope, id, props);


      const connection = new glue.Connection(this, 'GlueJobConnection', {
        type: glue.ConnectionType.NETWORK,
        vpc: props.vpc,
        securityGroups: props.securityGroups,
        subnet:props.subnets[0],
      });


      const ingest_job = new glue.Job(this, 'ingest-knowledge-from-s3',{
            executable: glue.JobExecutable.pythonShell({
            glueVersion: glue.GlueVersion.V1_0,
            pythonVersion: glue.PythonVersion.THREE_NINE,
            script: glue.Code.fromAsset(path.join(__dirname, '../../code/offline_process/aos_write_job.py')),
          }),
          jobName:'ingest_knowledge',
          maxConcurrentRuns:100,
          maxRetries:0,
          connections:[connection],
          maxCapacity:1,
          defaultArguments:{
              '--AOS_ENDPOINT':props.opensearch_endpoint,
              '--REGION':props.region,
              '--AOS_INDEX': "rag-data-index",
              '--additional-python-modules': 'boto3>=1.28.52,botocore>=1.31.52',
              '--bucket': '687752207838-24-04-10-02-26-15-aos-rag-bucket',
              '--object_key': 'kb/crosslingual_terminology.json,kb/multilingual_terminology.json'
          }
      })
      ingest_job.role.addToPrincipalPolicy(
        new iam.PolicyStatement({
              actions: [ 
                "sagemaker:InvokeEndpointAsync",
                "sagemaker:InvokeEndpoint",
                "s3:List*",
                "s3:Put*",
                "s3:Get*",
                "es:*",
                "bedrock:*",
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
              '--AOS_ENDPOINT':props.opensearch_endpoint,
              '--REGION':props.region,
              '--AOS_INDEX': "rag-data-index",
              '--additional-python-modules': 'boto3>=1.28.52,botocore>=1.31.52',
              '--model_id': 'anthropic.claude-3-sonnet-20240229-v1:0',
              '--object_key': 'src_files/chat_text.json',
              '--bucket': '687752207838-24-04-10-02-26-15-aos-rag-bucket',
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
                "es:*",
                "bedrock:*",
                ],
              effect: iam.Effect.ALLOW,
              resources: ['*'],
              })
      )
      this.jobArn = ingest_job.jobArn;
      this.jobName = ingest_job.jobName;
      this.ragJobName = rag_job.jobName
    }
}