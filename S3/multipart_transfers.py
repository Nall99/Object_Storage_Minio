from boto3.s3.transfer import TransferConfig
import dotenv
import boto3
import os

dotenv.load_dotenv()

# Set the desired multipart threshold value (5GB)
GB = 1024 ** 3
config = TransferConfig(multipart_threshold= 5 * GB)

# Perfom the transfer
s3 = boto3.client('s3',
                  endpoint_url=os.getenv('MINIO_ENDPOINT'),
                  aws_access_key_id=os.getenv('MINIO_KEY_ACCESS'),
                  aws_secret_access_key=os.getenv('MINIO_KEY_SECRET'))


s3.upload_file('large_file.txt', 'my-bucket', 'large_file.txt', Config=config)