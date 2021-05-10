import boto3, os
from .logging import Logger

logger = Logger.get_logger('modules/login.py', '')

class Login():
    def aws_session(profile):
        AWS_PROFILE = profile
        AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
        AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
        AWS_REGION = os.getenv('AWS_REGION')
        if  AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
            session = boto3.session.Session(
                aws_access_key_id = AWS_ACCESS_KEY_ID,
                aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
                region_name = AWS_REGION
            )
        else:
            logger.info("Using aws config from ~/.aws/config for profile: "  + AWS_PROFILE )
            session = boto3.Session(profile_name=AWS_PROFILE)

        return session