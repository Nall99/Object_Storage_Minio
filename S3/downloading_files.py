from botocore.exceptions import ClientError
import argparse
import logging
import dotenv
import boto3
import os

dotenv.load_dotenv()

def download_file(bucket_name, object_name, file_path="./"):
    """Download a file from an S3 bucket
    
    :param bucket_name: Name of the S3 bucket
    :param object_name: Name of the object to download
    :param file_path: Local path to save the downloaded file
    """

    # Se file_path for um diretório, monta o caminho completo usando o nome do objeto
    if file_path.endswith("/") or os.path.isdir(file_path):
        file_path = os.path.join(file_path, os.path.basename(object_name))
    
    # Download file
    try:
        s3_client = boto3.client('s3', 
                                 endpoint_url=os.getenv('MINIO_ENDPOINT'),
                                 aws_access_key_id=os.getenv('MINIO_KEY_ACCESS'),
                                 aws_secret_access_key=os.getenv('MINIO_KEY_SECRET'))
        
        s3_client.download_file(bucket_name, object_name, file_path)
    except ClientError as e:
        logging.error(e)
        return False
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download a file from an S3 bucket')
    parser.add_argument('bucket_name', help='Name of the S3 bucket')
    parser.add_argument('object_name', help='Name of the object to download')
    parser.add_argument('--file_path', default="./", help='Local path to save the downloaded file')
    args = parser.parse_args()

    sucesso = download_file(args.bucket_name, args.object_name, args.file_path)
    if sucesso:
        print(f'File "{args.object_name}" downloaded successfully from bucket "{args.bucket_name}" to "{args.file_path}".')
    else:
        print(f'Failed to download file "{args.object_name}" from bucket "{args.bucket_name}". Check logs for more details.')
