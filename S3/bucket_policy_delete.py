from botocore.exceptions import ClientError
import argparse
import logging
import dotenv
import boto3
import os

dotenv.load_dotenv()

def delete_bucket_policy(bucket_name, region='us-east-1'):
    """Delete the policy of an S3 bucket

    :param bucket_name: Name of the S3 bucket
    :param region: Region of the S3 bucket
    :return: True if the policy was deleted, else False
    """

    # Create an S3 client
    s3_client = boto3.client('s3', 
                             endpoint_url=os.getenv('MINIO_ENDPOINT'),
                             aws_access_key_id=os.getenv('MINIO_KEY_ACCESS'),
                             aws_secret_access_key=os.getenv('MINIO_KEY_SECRET'),
                             region_name=region)
    
    try:
        s3_client.delete_bucket_policy(Bucket=bucket_name)
        return True
    except ClientError as e:
        logging.error(e)
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Delete the policy of an S3 bucket')
    parser.add_argument('bucket_name', help='Name of the S3 bucket')
    parser.add_argument('--region', default='us-east-1', help='Region of the S3 bucket')
    args = parser.parse_args()

    sucesso = delete_bucket_policy(args.bucket_name, args.region)
    if sucesso:
        print(f'Bucket policy for "{args.bucket_name}" deleted successfully.')
    else:
        print(f'Failed to delete bucket policy for "{args.bucket_name}". Check logs for more details.')