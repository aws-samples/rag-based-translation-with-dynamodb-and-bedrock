#!/bin/bash

if [ "$#" -lt 1 ]||[ "$#" -gt 2 ]; then
    echo "usage: $0 [region-name] [account-id (optional)]"
    exit 1
fi

region=$1

if [ ! -n "$2" ]; then
    account_id=`aws sts get-caller-identity --query "Account" --output text`
else
    account_id="$2"
fi

ts=`date +%y-%m-%d-%H-%M-%S`
unique_tag="$account_id-$ts"

cn_region=("cn-north-1","cn-northwest-1")
if [[ "${cn_region[@]}" =~ "$region" ]]; then
    arn="arn:aws-cn:"
else
    arn="arn:aws:"
fi

bucket="${unique_tag}-aos-rag-bucket"

echo "CDK_DEFAULT_ACCOUNT=${account_id}" > .env
echo "CDK_DEFAULT_REGION=${region}" >> .env
echo "existing_vpc_id=optional" >> .env
echo "UPLOAD_BUCKET=${bucket}" >> .env
echo "UPLOAD_OBJ_PREFIX=aos-rag-content/" >> .env