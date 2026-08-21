import boto3
import dotenv
import os

dotenv.load_dotenv()

s3 = boto3.resource('s3',
                     endpoint_url=os.getenv('MINIO_ENDPOINT'),
                     aws_access_key_id=os.getenv('MINIO_KEY_ACCESS'),
                     aws_secret_access_key=os.getenv('MINIO_KEY_SECRET'))

for bucket in s3.buckets.all():
    print(bucket.name)