import boto3
import click
from botocore.exceptions import ClientError

session = boto3.Session(profile_name='pythonAutomation')
s3 = session.resource('s3')

@click.group()
# ------------------------------------------------------------------------------
def cli():
    "Webotron deploys websites to AWS"
    pass
# ------------------------------------------------------------------------------
@cli.command('list-buckets') #list all s3 buckets
def list_buckets():
    "List all s3 buckets"
    for bucket in s3.buckets.all():
        print(bucket)
# ------------------------------------------------------------------------------
@cli.command('list-bucket-objects') #list all objects in the bucket
@click.argument('bucket') #adding arg bucket name
def list_bucket_objects(bucket):
    "List objects in an s3 bucket"
    for obj in s3.Bucket(bucket).objects.all():
        print(obj)
# ------------------------------------------------------------------------------
@cli.command('setup-bucket')
@click.argument('bucket')
def setup_bucket(bucket):
    "Create and configure S3 bucket"

    #create S3 bucket (+handling exception in case bucket exists)
    try:
        s3_bucket = s3.create_bucket(Bucket=bucket)
    except ClientError as e:
        if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            s3_bucket = s3.Bucket(bucket)
    #create an S3 public policy
    policy = """{
    "Version":"2012-10-17",
    "Statement":[{
    "Sid":"PublicReadGetObject",
    "Effect":"Allow",
    "Principal": "*",
        "Action":["s3:GetObject"],
        "Resource":["arn:aws:s3:::%s/*"
    ]}]}""" % s3_bucket.name

    #assign a policy to s3 bucket
    pol = s3_bucket.Policy()
    pol.put(Policy=policy)

    #s3 website configuration
    ws = s3_bucket.Website()
    ws.put(WebsiteConfiguration={
        'ErrorDocument': {
            'Key': 'error.html'
        },
        'IndexDocument': {
            'Suffix': 'index.html'
        }
    })

    return
# ------------------------------------------------------------------------------

if __name__ == '__main__':
    cli()
