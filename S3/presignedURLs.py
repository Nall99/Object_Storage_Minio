from botocore.exceptions import ClientError
from botocore.config import Config
import argparse
import logging
import dotenv
import boto3
import os

dotenv.load_dotenv()

def create_presigned_url(bucket_name, object_name, region_name='us-east-1', expiration = 3600):
    """ Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param region_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, return None.
    """

    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3',
                             endpoint_url=os.getenv('MINIO_ENDPOINT'),
                             aws_access_key_id=os.getenv('MINIO_KEY_ACCESS'),
                             aws_secret_access_key=os.getenv('MINIO_KEY_SECRET'),
                             region_name=region_name,
                             config=Config(
                                     signature_version='s3v4',
                                     s3={'addressing_style': 'path'}
                             ))
    try:
        response = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': object_name},
            ExpiresIn=expiration
        )
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a presigned URL for an S3 object')
    parser.add_argument('bucket_name', help='Name of the S3 bucket')
    parser.add_argument('object_name', help='Name of the object to generate a presigned URL for')
    parser.add_argument('--region_name', default='us-east-1', help='Region of the S3 bucket')
    parser.add_argument('--expiration', type=int, default=3600, help='Time in seconds for the presigned URL to remain valid (default: 3600)')
    args = parser.parse_args()

    url = create_presigned_url(args.bucket_name, args.object_name, args.region_name, args.expiration)
    if url:
        print(f'Presigned URL: {url}')
    else:
        print(f'Failed to generate presigned URL for object "{args.object_name}" in bucket "{args.bucket_name}". Check logs for more details.')