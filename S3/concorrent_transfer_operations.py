from boto3.s3.transfer import TransferConfig
import dotenv
import boto3
import os

dotenv.load_dotenv()

# To consume less downstream bandwith, decrease the maximum concurrency
config = TransferConfig(max_concurrency=5)

# Download an S3 object
s3 = boto3.client('s3',
                  endpoint_url=os.getenv('MINIO_ENDPOINT'),
                  aws_access_key_id=os.getenv('MINIO_KEY_ACCESS'),
                  aws_secret_access_key=os.getenv('MINIO_KEY_SECRET'))

s3.download_file('minio-s3-demo-bucket', 'guaxinim-demo', os.path.join("./", os.path.basename('guaxinim-demo')), Config=config)