import boto3
from login import Login


class S3:
    def s3():
        session = Login.aws_session()
        s3_client = session.client("s3")
        list_of_bucket = s3_client.list_buckets()
        for bucket in list_of_bucket["Buckets"]:
            print(f'  {bucket["Name"]}')

    def s3_2():
        tempCredentials = Login.aws_temp_session()
        s3_connection = Session(
            aws_access_key_id=tempCredentials.access_key,
            aws_secret_access_key=tempCredentials.secret_key,
            security_token=tempCredentials.session_token,
        )

        return s3_connection
