import dotenv
import boto3
import os

dotenv.load_dotenv()

s3 = boto3.client('s3',
                  endpoint_url=os.getenv('MINIO_ENDPOINT'),
                  aws_access_key_id=os.getenv('MINIO_KEY_ACCESS'),
                  aws_secret_access_key=os.getenv('MINIO_KEY_SECRET'))

response = s3.list_buckets()
print("Buckets disponíveis:")
for bucket in response['Buckets']:
    print(f'  {bucket["Name"]}')