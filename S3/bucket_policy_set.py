import dotenv
import boto3
import os
import json

dotenv.load_dotenv()

# Create a bucket policy
bucket_name = 'minio-s3-demo-bucket'
bucket_policy = {
    'Version': '2012-10-17',
    'Statement': [{
        'Sid': 'AddPerm',
        'Effect': 'Allow',
        'Principal': '*',
        'Action': ['s3:GetObject'],
        'Resource': [f'arn::s3:::{bucket_name}/*']
    }]
}

# Convert the policy from JSON dict to string
bucket_policy_str = json.dumps(bucket_policy)

# Set the policy
s3 = boto3.client('s3',
                  endpoint_url=os.getenv('MINIO_ENDPOINT'),
                  aws_access_key_id=os.getenv('MINIO_KEY_ACCESS'),
                  aws_secret_access_key=os.getenv('MINIO_KEY_SECRET'))
s3.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy_str)