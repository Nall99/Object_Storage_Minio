from botocore.exceptions import ClientError
import argparse
import logging
import dotenv
import boto3
import os

dotenv.load_dotenv()

def retrieve_website_configuration(bucket_name, region_name='us-east-1'):
    """ Retrieve the website configuration for an S3 bucket

    :param bucket_name: Name of the S3 bucket
    :param region_name: Region of the S3 bucket
    :return: Dictionary with website configuration
    """

    # Create an S3 client
    s3 = boto3.client('s3',
                      endpoint_url=os.getenv('MINIO_ENDPOINT'),
                      aws_access_key_id=os.getenv('MINIO_KEY_ACCESS'),
                      aws_secret_access_key=os.getenv('MINIO_KEY_SECRET'),
                      region_name=region_name)

    # retrieve a bucket's website configuration
    try:
        result = s3.get_bucket_website(Bucket=bucket_name)
        
    except ClientError as e:
        logging.error(e)
        return None

    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Retrieve the website configuration for an S3 bucket')
    parser.add_argument('bucket_name', help='Name of the S3 bucket')
    parser.add_argument('--region_name', default='us-east-1', help='Region of the S3 bucket')
    args = parser.parse_args()

    website_config = retrieve_website_configuration(args.bucket_name, args.region_name)
    if website_config:
        print(f'Website configuration for bucket "{args.bucket_name}": {website_config}')
    else:
        print(f'Failed to retrieve website configuration for bucket "{args.bucket_name}". Check logs for more details.')