import boto3
from botocore.exceptions import ClientError

from app.core.config import settings


def generate_presigned_upload_url(object_key: str, expiration: int = 3600) -> str:
    """
    Returns a presigned URL the client uses to upload directly to S3.
    The API doesn't handle image bytes, this keeps each server stateless
    and avoids doubling bandwidth through the API tier.
    """
    client = boto3.client(
        "s3",
        region_name=settings.aws_region,
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
    )

    try:
        url = client.generate_presigned_url(
            "put_object",
            Params={"Bucket": settings.s3_bucket_name, "Key": object_key},
            ExpiresIn=expiration,
        )
    except ClientError as e:
        raise RuntimeError(f"Failed to generate presigned URL: {e}") from e

    return url
