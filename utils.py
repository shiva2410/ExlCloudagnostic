from boto3.session import Session
import boto3
import os
import pyshorteners
from azure.storage.blob import BlobServiceClient, BlobClient
from azure.storage.blob import ContentSettings, ContainerClient
from azure.storage.blob import generate_blob_sas
from azure.storage.blob import BlobSasPermissions
from datetime import datetime, timedelta
import oss2
import logging
from botocore.exceptions import ClientError
import botocore
import os
type_tiny = pyshorteners.Shortener()

"""
Credentials Handling for AWS, Azure & Alibaba

"""

# AWS Credentials can be setup in the CLI using command - "AWS configure"

main_account_name = os.environ["azure_account_name"]  #Azure
main_account_key = os.environ["azure_account_key"]

access_key_id=os.environ['alibaba_access_key_id']  #Alibaba
access_key_secret=os.environ['alibaba_access_key_secret']


MY_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName="+str(main_account_name)+";AccountKey="+str(main_account_key)+";EndpointSuffix=core.windows.net"
path = os.getcwd()
LOCAL_BLOB_PATH = str(path)
blob_service_client =  BlobServiceClient.from_connection_string(MY_CONNECTION_STRING)
endpoint = 'oss-ap-south-1.aliyuncs.com' 


"""
AWS METHODS TO UPLOAD, LIST FILES IN A BUCKET, DOWNLOAD FILES & CREATE TEMPORARY DOWNLOAD LINK OF FILES

"""

def download_file_aws(bucket_name,filename):     #Function to Download files from AWS Bucket
	s3 = boto3.resource('s3')   # Creating session for s3 resource
	try:
		s3.Bucket(bucket_name).download_file(filename,filename)  
	except botocore.exceptions.ClientError as e:
		if e.response['Error']['Code'] == "404":
			print("The object does not exist.")
			return 'No such object found'
		else:
			raise
	return os.path.join(os.getcwd(),filename)

def upload_file_aws(bucket_name,filename):      #Function to Upload file to AWS Bucket
	s3_client = boto3.client('s3') # Creating session for s3 resource
	try:
		response = s3_client.upload_file(filename, bucket_name, filename)
	except ClientError as e:
		logging.error(e)
		return False

def list_items_aws_bucket(bucket_name): # prints the contents of bucket
	items=[]
	s3 = boto3.client('s3') # Creating session for s3 resource
	for key in s3.list_objects(Bucket=bucket_name)['Contents']:  #iterating in items present in a bucket
		items.append(key['Key'])
	return items

def download_file_temp_aws(bucket_name,filename,expiration_time):  #Function to get temporary file download link
	s3_client = boto3.client('s3') # Creating session for s3 resource
	try:
		s3 = boto3.resource('s3')
		if s3.Bucket(bucket_name) in s3.buckets.all():
			long_url = s3_client.generate_presigned_url('get_object',Params={'Bucket': bucket_name, 'Key': filename},ExpiresIn=expiration_time)
			print(long_url)
			try:
				short_url = type_tiny.tinyurl.short(long_url)
				return short_url
			except:
				return long_url
		else:
			return 'No such object found'
	except Exception as e:
		print(e)
		return 'No such object found'

"""
AZURE METHODS TO UPLOAD, LIST FILES IN A BUCKET, DOWNLOAD FILES & CREATE TEMPORARY DOWNLOAD LINK OF FILES

"""

def upload_file_azure(MY_FILE_CONTAINER,localpath): # AZURE Function to upload files
	try:
		file_name = os.path.basename(localpath)
		blob_client = blob_service_client.get_blob_client(container=MY_FILE_CONTAINER, blob=file_name)
		
		with open(localpath, "rb") as data:
			blob_client.upload_blob(data,overwrite=True)
		return "File uploaded successfully"
	except:
		return "Something went wrong"

def download_file_azure(MY_FILE_CONTAINER,blobname): # AZURE Function to download files for authorized users
	try:
		blob_client = blob_service_client.get_container_client(container= MY_FILE_CONTAINER)
		data = blob_client.get_blob_client(blobname).download_blob().readall()
		download_file_path = os.path.join(LOCAL_BLOB_PATH, blobname)
		with open(download_file_path, "wb") as file:
			file.write(data)
		return download_file_path
	except:
		return 'No such object found'

def download_file_temp_azure(MY_FILE_CONTAINER,blobname,expirytime): # AZURE Function to download files temporarily for unauthorized users
	try:
		blob_client = blob_service_client.get_container_client(container= MY_FILE_CONTAINER)
		if blob_client.exists() != False:
			blob_file = blob_client.get_blob_client(blobname)
			if blob_file.exists() != False:
				perm_url = blob_file.url
				sas_blob = generate_blob_sas(account_name= main_account_name, 
									container_name= MY_FILE_CONTAINER,
									blob_name= blobname,
									account_key= main_account_key,
									permission=BlobSasPermissions(read=True, write= False, create= False),
									expiry=datetime.utcnow() + timedelta(seconds=expirytime))
				url_with_sas = f"{perm_url}?{sas_blob}"
				try:
					short_url = type_tiny.tinyurl.short(url_with_sas)
					return short_url
				except:
					return url_with_sas
			else:
				return 'No such object found'
		else:
			return 'No such object found'
	except Exception as e:
		print(e)
		return 'No such object found'

def list_items_azure_bucket(MY_FILE_CONTAINER): # AZURE Function to view files inside Container
	list_of_files=[]
	my_container = blob_service_client.get_container_client(container= MY_FILE_CONTAINER)
	my_blobs = my_container.list_blobs()
	for blob in my_blobs:
		list_of_files.append(blob.name)
	return list_of_files

"""
ALIBABA METHODS TO UPLOAD, LIST FILES IN A BUCKET, DOWNLOAD FILES & CREATE TEMPORARY DOWNLOAD LINK OF FILES

"""

def upload_file_alibaba(bucket_name,mainpath):  # ALIBABA Upload the file using file name and bucket name as parameter
	bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)
	head, filepath = os.path.split(mainpath)
	try:

		with open(filepath, "rb") as f:
			data = f.read()
			bucket.put_object(filepath , data)  # data can be a any file
			return "Upload Successfully"
	except:
		return "Upload correct file"

def download_file_alibaba(bucket_name,filepath):  # ALIBABA Download the file using file name and bucket name as parameter
	bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)
	try:
		ret=bucket.get_object_to_file(filepath, filepath) # file downloaded to current directory
	except:
		return 'No such object found'
	return os.path.join(os.getcwd(),filepath) if ret.status==200 else 0 # returning path of current directory

def download_file_temp_alibaba(bucket_name,filepath,expiration_time): # temporary downloading functionality using file name and bucket name as parameter
	bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)
	try:
		ret=bucket.get_object_to_file(filepath, filepath)
		ret_link = bucket.sign_url('GET', filepath,expiration_time)  # The return value is the link, the parameters are in order, method/file path on oss/expiration time(s) which is 60 sec
		try:
			type_tiny = pyshorteners.Shortener() #shortening link to protect data
			short_url = type_tiny.tinyurl.short(ret_link)
			return short_url
		except:
			return ret_link
	except Exception as e:
		print(e)
		return 'No such object found'


def list_items_alibaba_bucket(bucket_name):  # ALIBABA list all the objects in the bucket using bucket name
	bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)
	objects_cloud=[]
	for obj in oss2.ObjectIterator(bucket):
		objects_cloud.append(obj.key)
	return objects_cloud

