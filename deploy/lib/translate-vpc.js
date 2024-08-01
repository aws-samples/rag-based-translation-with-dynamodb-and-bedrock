import { CfnOutput, NestedStack } from 'aws-cdk-lib';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as dotenv from "dotenv";
dotenv.config();

export class VpcStack extends NestedStack {

    vpc;
    subnets;
    /**
     *
     * @param {Construct} scope
     * @param {string} id
     * @param {StackProps=} props
     */
    constructor(scope, id, props) {
        super(scope, id, props);
        const existing_vpc_id = props.env.existing_vpc_id;


        //create a new vpc
        if (!existing_vpc_id || existing_vpc_id === 'optional') {
            this.vpc = new ec2.Vpc(this, 'Rag-Based-Translate-VPC', {
                ipAddresses: ec2.IpAddresses.cidr('10.22.0.0/16'),
                maxAzs: 2,
            });
        }
        else {
            this.vpc = ec2.Vpc.fromLookup(
                this, 'Rag-Based-Translate-VPC',
                {
                    vpcId: existing_vpc_id,
                }
            )
        }
        this.subnets = this.vpc.privateSubnets;

    }
}