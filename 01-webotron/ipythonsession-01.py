# coding: utf-8
import boto3
session = boto3.Session(profile_name='pythonAutomation')

# create an s3 session
s3 = session.resource('s3')

# show all buckets
for bucket in s3.buckets.all():
    print(bucket)

# create a new s3 bucket     
# new_bucket = s3.create_bucket(Bucket='somerandombucketnamemfjksdnfu34j9f8')

