from modules.get_s3 import S3

s3_connection = S3.s3_2()
bucket = s3_connection.get_bucket(bucket_name="cluster")
objectlist = bucket.list()
for obj in objectlist:
    print( obj.name)