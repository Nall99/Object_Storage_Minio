from botocore.exceptions import ClientError
import argparse
import logging
import dotenv
import boto3
import os

dotenv.load_dotenv()

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # Se object_name não for especificado, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Da upload do arquivo
    s3_client = boto3.client('s3',
                             endpoint_url=os.getenv('MINIO_ENDPOINT'),
                             aws_access_key_id=os.getenv('MINIO_KEY_ACCESS'),
                             aws_secret_access_key=os.getenv('MINIO_KEY_SECRET'))
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Faz upload de um arquivo para um bucket no MinIO/S3')
    parser.add_argument('file_name', help='Nome do arquivo a ser enviado')
    parser.add_argument('bucket', help='Nome do bucket de destino')
    parser.add_argument('--object_name', help='Nome do objeto no S3 (opcional)')
    args = parser.parse_args()

    sucesso = upload_file(args.file_name, args.bucket, args.object_name)
    if sucesso:
        print(f'Arquivo "{args.file_name}" enviado com sucesso para o bucket "{args.bucket}".')
    else:
        print(f'Falha ao enviar o arquivo "{args.file_name}" para o bucket "{args.bucket}". Verifique os logs para mais detalhes.')