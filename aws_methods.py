from boto3.session import Session
import boto3
import os

# ACCESS_KEY = 'AKIAY6KCSSCHL63PJUEF'
# SECRET_KEY = 'JI9/i4jdBa764P4xGM6ZVAv0CyLFO6OAiXM8A6m'

# ACCESS_KEY = 'AKIAY6KCSSCHCRJ7BGO4'
# SECRET_KEY = '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'

def download_file_aws(bucket_name,filename):
	session = Session(aws_access_key_id=ACCESS_KEY,
	              aws_secret_access_key=SECRET_KEY)
	s3 = session.resource('s3')
	your_bucket = s3.Bucket('exlhackathon')

	s3 = boto3.client ('s3')
	your_bucket.download_file(filename,filename)
	return os.path.join(os.getcwd(),filename)

def upload_file_aws(bucket_name,filename):
	try:
		session = Session(aws_access_key_id=ACCESS_KEY,
	              aws_secret_access_key=SECRET_KEY)
		s3 = session.resource('s3')
		Filename='kpmg.gif'
		Bucket='exlhackathon'
		Key="/uploads/" 
		s3.meta.client.upload_file(Filename=Filename, Bucket=Bucket, Key=Filename)
		return 'Success'
	except Exception as e:
		return e

def list_items_aws_bucket(bucket_name): # prints the contents of bucket
	items=[]
	session = Session(aws_access_key_id=ACCESS_KEY,
	              aws_secret_access_key=SECRET_KEY)
	s3 = session.resource('s3')
	your_bucket = s3.Bucket('exlhackathon')

	for s3_file in your_bucket.objects.all():
	    items.append(s3_file.key)
	return items

filename='kpmg.gif'
bucket_name='exlhackathon'
print(download_file_aws(bucket_name,filename))
print(upload_file_aws(bucket_name,filename))
print(list_items_aws_bucket(bucket_name))