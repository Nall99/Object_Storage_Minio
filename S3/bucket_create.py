from botocore.exceptions import ClientError
import argparse
import logging
import dotenv
import boto3
import os

dotenv.load_dotenv()

def create_bucket(bucket_name, region='us-east-1'):
    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """

    # Create bucket
    try:
        bucket_config = {}
        s3_client = boto3.client('s3', 
                                 endpoint_url=os.getenv('MINIO_ENDPOINT'),
                                 aws_access_key_id=os.getenv('MINIO_KEY_ACCESS'),
                                 aws_secret_access_key=os.getenv('MINIO_KEY_SECRET'),
                                 region_name=region)
        if region != 'us-east-1':
            bucket_config['CreateBucketConfiguration'] = {'LocationConstraint': region}
        s3_client.create_bucket(Bucket=bucket_name, **bucket_config)
    except ClientError as e:
        logging.error(e)
        return False
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Cria um bucket no MinIO/S3')
    parser.add_argument('bucket_name', help='Nome do bucket a ser criado')
    parser.add_argument('--region', default='us-east-1', help='Região do bucket')
    args = parser.parse_args()

    sucesso = create_bucket(args.bucket_name, args.region)
    if sucesso:
        print(f'Bucket "{args.bucket_name}" criado com sucesso na região "{args.region}".')
    else:
        print(f'Falha ao criar o bucket "{args.bucket_name}". Verifique os logs para mais detalhes.')