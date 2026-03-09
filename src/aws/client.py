import boto3
import json
import logging
import os
from botocore.exceptions import ClientError
from botocore.config import Config

logger = logging.getLogger(__name__)

class AWSClientManager:
    """Manages AWS service connections using boto3."""
    
    def __init__(self, region_name: str = "us-east-1"):
        # Configure standard retries
        my_config = Config(
            region_name=region_name,
            retries={
                'max_attempts': 3,
                'mode': 'standard'
            }
        )
        self.region_name = region_name
        
        # Initialize clients lazily
        self._s3_client = None
        self._bedrock_client = None
        self._bedrock_runtime_client = None

    @property
    def s3(self):
        if self._s3_client is None:
            self._s3_client = boto3.client('s3', region_name=self.region_name)
        return self._s3_client

    @property
    def bedrock(self):
        if self._bedrock_client is None:
            self._bedrock_client = boto3.client('bedrock', region_name=self.region_name)
        return self._bedrock_client
        
    @property
    def bedrock_runtime(self):
        if self._bedrock_runtime_client is None:
            self._bedrock_runtime_client = boto3.client('bedrock-runtime', region_name=self.region_name)
        return self._bedrock_runtime_client


aws_manager = AWSClientManager()


def upload_to_s3(bucket_name: str, object_name: str, data: dict) -> bool:
    """Upload data to S3 bucket."""
    try:
        aws_manager.s3.put_object(
            Bucket=bucket_name,
            Key=object_name,
            Body=json.dumps(data)
        )
        logger.info(f"Successfully uploaded {object_name} to {bucket_name}")
        return True
    except ClientError as e:
        logger.error(f"Error uploading to S3: {e}")
        return False

def download_from_s3(bucket_name: str, object_name: str) -> dict | None:
    """Download data from S3 bucket."""
    try:
        response = aws_manager.s3.get_object(Bucket=bucket_name, Key=object_name)
        return json.loads(response['Body'].read().decode('utf-8'))
    except ClientError as e:
        logger.error(f"Error downloading from S3: {e}")
        return None
