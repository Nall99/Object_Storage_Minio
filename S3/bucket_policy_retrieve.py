import argparse
import logging
import dotenv
import boto3
import os

dotenv.load_dotenv()

def retrieve_bucket_policy(bucket_name, region='us-east-1'):
    """Retrieve the policy of an S3 bucket

    :param bucket_name: Name of the S3 bucket
    :param region: Region of the S3 bucket
    :return: The bucket policy as a string, or None if an error occurs
    """

    # Create an S3 client
    s3_client = boto3.client('s3', 
                             endpoint_url=os.getenv('MINIO_ENDPOINT'),
                             aws_access_key_id=os.getenv('MINIO_KEY_ACCESS'),
                             aws_secret_access_key=os.getenv('MINIO_KEY_SECRET'),
                             region_name=region)
    
    try:
        response = s3_client.get_bucket_policy(Bucket=bucket_name)
        return response['Policy']
    except Exception as e:
        logging.error(e)
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Retrieve the policy of an S3 bucket')
    parser.add_argument('bucket_name', help='Name of the S3 bucket')
    parser.add_argument('--region', default='us-east-1', help='Region of the S3 bucket')
    args = parser.parse_args()

    policy = retrieve_bucket_policy(args.bucket_name, args.region)
    if policy:
        print(f'Bucket Policy for "{args.bucket_name}":\n{policy}')
    else:
        print(f'Failed to retrieve bucket policy for "{args.bucket_name}". Check logs for more details.')