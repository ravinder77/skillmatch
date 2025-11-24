import uuid

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from fastapi import UploadFile

s3_client = boto3.client("s3")


def upload_file_to_s3(file: UploadFile, bucket_name: str, candidate_id: int) -> str:
    try:
        file_extension = file.filename.split(".")[-1]
        file_key = f"resumes/{candidate_id}{uuid.uuid4()}/{file.filename}"

        s3_client.upload_fileobj(
            file.file,
            bucket_name,
            file_key,
            ExtraArgs={"ContentType": file.content_type, "ACL": "private"},
        )

        return file_key  # store key in db
    except (BotoCoreError, ClientError) as e:
        raise RuntimeError(f"Error uploading file to S3: {str(e)}")
