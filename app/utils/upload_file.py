import uuid
import boto3
from fastapi import UploadFile

def upload_file_to_s3(file: UploadFile, bucket_name: str, user_id: int) -> str:
    file_extension = file.filename.split('.')[-1]
    file_key = f"resumes/{user_id}{uuid.uuid4()}.{file_extension}"


    s3_client = boto3.client('s3')

    s3_client.upload_file(
        file.file,
        bucket_name,
        file_key,
        ExtraArgs={"ContentType": file.content_type, "ACL": "private"},
    )

    return file_key  # store key in db


