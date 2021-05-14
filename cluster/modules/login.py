import boto3, os, time

class Login():
    def aws_session(profile, logger):
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
            logger.info("Creating session for profile: "  + AWS_PROFILE )
            session = boto3.Session(profile_name=AWS_PROFILE)

        return session