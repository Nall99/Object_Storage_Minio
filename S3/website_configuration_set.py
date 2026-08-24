import dotenv
import boto3
import os

dotenv.load_dotenv()

# Define the website configuration
website_configuration = {
    'ErrorDocument': {'Key': 'error.html'},
    'IndexDocument': {'Suffix': 'index.html'},
}

# Set the website configurtion
s3 = boto3.client('s3',
                  endpoint_url=os.getenv('MINIO_ENDPOINT'),
                  aws_access_key_id=os.getenv('MINIO_KEY_ACCESS'),
                  aws_secret_access_key=os.getenv('MINIO_KEY_SECRET'),
                  region_name='us-east-1')
s3.put_bucket_website(Bucket=os.getenv('MINIO_BUCKET_NAME'), WebsiteConfiguration=website_configuration)