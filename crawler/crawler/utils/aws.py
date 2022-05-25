"""This module contains AWS-Related utility functions"""
import boto3

from typing import IO


class S3AuthenticationException(Exception):
    pass


class S3Client:
    _AWS_ACCESS_KEY = None
    _AWS_SECRET_KEY = None
    _REGION_NAME = None
    _S3_BUCKET = None
    client = None

    def __init__(self,
                 access_key: str,
                 secret_key: str,
                 region_name: str,
                 bucket_name: str):
        self._AWS_ACCESS_KEY = access_key
        self._AWS_SECRET_KEY = secret_key
        self._REGION_NAME = region_name
        self._S3_BUCKET = bucket_name

    def login(self):
        """Setup S3 Client"""
        session = boto3.session.Session(
            aws_access_key_id=self._AWS_ACCESS_KEY,
            aws_secret_access_key=self._AWS_SECRET_KEY,
            region_name=self._REGION_NAME
        )
        self.client = session.client('s3')

    def upload(self,
               data: IO,
               file_name: str) -> bool:
        """Upload file-like object to S3 Bucket

        Args:
            data (IO): specify the stream to be uploaded.
            file_name (str): specify the file name in S3 bucket.

        Returns:
            (bool): True if success, otherwise, False.
        """
        if self.client is None:
            raise S3AuthenticationException('Unauthorized client')
        try:
            self.client.upload_fileobj(
                data,
                self._S3_BUCKET,
                file_name
            )
        except Exception as e:
            return False
        else:
            return True
