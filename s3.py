import boto3
from dotenv import load_dotenv
load_dotenv()

class S3:
    """Handles operations related to an S3 bucket."""

    s3 = boto3.client(
        "s3",
        "us-west-1"
    )

    def __init__(self, s3):
        self.s3 = s3

    @classmethod
    def get_bucket_name(cls):
        """Retrieve the first bucket name in the AWS account."""
        return cls.s3.list_buckets()['Buckets'][0]['Name']

    @classmethod
    def get_presigned_url(cls, obj_key, expiration=172800):
        """
        Generate a presigned URL to share an S3 object.

        Parameters:
            obj_key (str): The object's key in the bucket.
            expiration (int): URL's expiration time in seconds.
            Default is ~2 days.

        Returns:
            str: Presigned URL.
        """
        bucket = cls.get_bucket_name()
        url = cls.s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': bucket, 'Key': obj_key},
            ExpiresIn=expiration)
        return url

    @classmethod
    def upload_file(cls, file_name, save_as_name):
        """
        Upload a file-like object to the S3 bucket.

        Parameters:
            file_obj (file-like object): The object to upload.
            save_as_name (str): The name to save the object as in S3.
        """
        bucket = cls.get_bucket_name()
        file_name.seek(0)
        cls.s3.upload_fileobj(file_name, bucket, save_as_name)

    @classmethod
    def download_file(cls, file_name, save_as_name):
        """
        Download a file from the S3 bucket.

        Parameters:
            source_key (str): The key (path) of the object in S3.
            destination_path (str): Local path to save the downloaded object.
        """
        bucket = cls.get_bucket_name()
        cls.s3.download_file(bucket, file_name, save_as_name)