from botocore.exceptions import ClientError
import argparse
import logging
import dotenv
import boto3
import os

dotenv.load_dotenv()

def access_permissions(bucket_name, region_name='us-east-1'):
    """ Check access permissions for an S3 bucket
    
    :param bucket_name: Name of the S3 bucket
    :param region_name: Region of the S3 bucket
    :return: Dictionary with access permissions
    """

    # Create an S3 client
    s3 = boto3.client('s3',
                      endpoint_url=os.getenv('MINIO_ENDPOINT'),
                      aws_access_key_id=os.getenv('MINIO_KEY_ACCESS'),
                      aws_secret_access_key=os.getenv('MINIO_KEY_SECRET'),
                      region_name=region_name)

    # retrieve a bucket's ACL
    try:
        result = s3.get_bucket_acl(Bucket=bucket_name)
        
    except ClientError as e:
        logging.error(e)
        return None

    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check access permissions for an S3 bucket')
    parser.add_argument('bucket_name', help='Name of the S3 bucket')
    parser.add_argument('--region_name', default='us-east-1', help='Region of the S3 bucket')
    args = parser.parse_args()

    permissions = access_permissions(args.bucket_name, args.region_name)
    if permissions:
        print(f'Access permissions for bucket "{args.bucket_name}": {permissions}')
    else:
        print(f'Failed to retrieve access permissions for bucket "{args.bucket_name}". Check logs for more details.')