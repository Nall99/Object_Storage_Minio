from botocore.exceptions import ClientError
from botocore.config import Config
import logging
import dotenv
import boto3
import os

dotenv.load_dotenv()

def create_presigned_post(
        bucket_name,
        object_name,
        region_name='us-east-1',
        fields=None,
        conditions=None,
        expiration=3600
        ):
    """Generate a presigned URL S3 POST request to upload a file
    
    :param bucket_name: string
    :param object_name: string
    :param region_name: string
    :param fields: Dictionary of prefilled form fields
    :param conditions: List of conditions to include in the policy
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Dictionary with the following keys:
        url: URL to post to
        fields: Dictionary of form fields and values to submit with the POST
    :return: None if error.
    """

    # Generate a presigned S3 POST URL
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
        response = s3_client.generate_presigned_post(
            Bucket=bucket_name,
            Key=object_name,
            Fields=fields,
            Conditions=conditions,
            ExpiresIn=expiration
        )
    except ClientError as e:
        logging.error(e)
        return None

    return response

# import requests

# # Generate a presigned S3 POST URL
# object_name = 'guaxinim-demo'
# response = create_presigned_post('minio-s3-demo-bucket', object_name)
# if response is None:
#     exit(1)

# # Demonstrate how another Python program can use the presigned URL to upload a file
# with open(object_name, 'rb') as f:
#     files = {'file': (object_name, f)}
#     http_response = requests.post(response['url'], data=response['fields'], files=files)

# # If successful, returns HTTP status code 204
# print(f'File upload HTTP status code: {http_response.status_code}')


def generate_html_form(presigned_data, output_path='upload_form.html'):
    """Gera um arquivo HTML pronto pra upload direto no bucket via navegador"""

    hidden_inputs = ""
    for name, value in presigned_data['fields'].items():
        hidden_inputs += f'    <input type="hidden" name="{name}" value="{value}" />\n'

    html = f"""<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  </head>
  <body>
    <form action="{presigned_data['url']}" method="post" enctype="multipart/form-data">
{hidden_inputs}    File:
      <input type="file" name="file" /> <br />
      <input type="submit" name="submit" value="Upload to Bucket" />
    </form>
  </body>
</html>
"""

    with open(output_path, 'w') as f:
        f.write(html)

    print(f'Formulário HTML gerado em: {output_path}')


if __name__ == "__main__":
    object_name = 'guaxinim-demo'
    response = create_presigned_post('minio-s3-demo-bucket', object_name)

    if response is None:
        exit(1)

    generate_html_form(response)