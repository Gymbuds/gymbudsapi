import boto3
import os
from dotenv import load_dotenv
from uuid import uuid4

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
BUCKET_NAME = os.getenv("AWS_S3_BUCKET")

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
)

def create_presigned_upload_url(user_id: int, file_extension: str, folder: str = "profile_pictures", expiration: int = 3600):
    key = f"{folder}/user_{user_id}_{uuid4()}.{file_extension}"

    try:
        presigned_url = s3_client.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": BUCKET_NAME,
                "Key": key,
                "ContentType": f"image/{file_extension}",
            },
            ExpiresIn=expiration,
        )
        s3_file_url = f"https://{BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{key}"
        return presigned_url, s3_file_url

    except Exception as e:
        print(f"Error generating presigned URL: {e}")
        return None, None
