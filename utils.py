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
import os
type_tiny = pyshorteners.Shortener()

main_account_name = 'exltrinity'
main_account_key = 'JyH+zU96WW39aL2BeXk20MGj1f1hyeoEzT0qzDqeEVr0dGiqnewYfEOk/VUt01YWi/Yus81IHW+2+AStiKmUnA==' #Azure

MY_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName="+str(main_account_name)+";AccountKey="+str(main_account_key)+";EndpointSuffix=core.windows.net"
path = os.getcwd()
LOCAL_BLOB_PATH = str(path)
blob_service_client =  BlobServiceClient.from_connection_string(MY_CONNECTION_STRING)

access_key_id = 'LTAI5tMMRGbFNaHsoC16c2dc'   #Alibaba
access_key_secret = 'kV8oIJaomxMSAmycOTbQiDTv59HliT'
endpoint = 'oss-ap-south-1.aliyuncs.com' 
# bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name) # Create Alibaba Object for this bucket

# ACCESS_KEY = 'AKIAY6KCSSCHCRJ7BGO4'
# SECRET_KEY = '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'

def download_file_aws(bucket_name,filename):     #Function to Download files from AWS Bucket
	s3 = boto3.resource('s3')
	try:
	    s3.Bucket(bucket_name).download_file(filename,filename)
	except botocore.exceptions.ClientError as e:
	    if e.response['Error']['Code'] == "404":
	        print("The object does not exist.")
	    else:
	        raise
	return os.path.join(os.getcwd(),filename)

def upload_file_aws(bucket_name,filename):      #Function to Upload file to AWS Bucket
	s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(filename, bucket_name, filename)
    except ClientError as e:
        logging.error(e)
        return False
    return return 'Success'

def list_items_aws_bucket(bucket_name): # prints the contents of bucket
	items=[]
	s3 = boto3.client('s3')
	for key in s3.list_objects(Bucket=bucket_name)['Contents']:
		items.append(key['Key'])
	return items

def download_file_temp_aws(bucket_name,filename,expiration_time):  #Function to get temporary file download link
	s3_client = boto3.client('s3')
	long_url = s3_client.generate_presigned_url('get_object',Params={'Bucket': bucket_name, 'Key': filename},ExpiresIn=expiration_time)
	try:
		short_url = type_tiny.tinyurl.short(long_url)
		return short_url
	except:
		return long_url


def upload_file_azure(MY_FILE_CONTAINER,localpath): # Function to upload files
	try:
		file_name = os.path.basename(localpath)
		blob_client = blob_service_client.get_blob_client(container=MY_FILE_CONTAINER, blob=file_name)
		
		with open(localpath, "rb") as data:
			blob_client.upload_blob(data,overwrite=True)
		return "File uploaded successfully"
	except:
		return "Something went wrong"

def download_file_azure(MY_FILE_CONTAINER,blobname): # Function to download files for authorized users
	try:
		blob_client = blob_service_client.get_container_client(container= MY_FILE_CONTAINER)
		data = blob_client.get_blob_client(blobname).download_blob().readall()
		download_file_path = os.path.join(LOCAL_BLOB_PATH, blobname)
		with open(download_file_path, "wb") as file:
			file.write(data)
		return download_file_path
	except:
		return "Something went wrong"

def download_file_temp_azure(MY_FILE_CONTAINER,blobname,expirytime): # Function to download files temporarily for unauthorized users
	try:
		blob_client = blob_service_client.get_container_client(container= MY_FILE_CONTAINER)
		blob_file = blob_client.get_blob_client(blobname)
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
	except Exception as e:
		print(e)
		return "Something went wrong"

def list_items_azure_bucket(MY_FILE_CONTAINER): # Function to view files inside Container
	try:
		list_of_files=[]
		my_container = blob_service_client.get_container_client(container= MY_FILE_CONTAINER)
		my_blobs = my_container.list_blobs()
		for blob in my_blobs:
			list_of_files.append(blob.name)
		return list_of_files
	except Exception as e:
		print(e)
		return "Something went Wrong"
 
def upload_file_alibaba(bucket_name,mainpath):  # Upload the file using file name and bucket name as parameter
	bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)
	head, filepath = os.path.split(mainpath)
	try:

		with open(filepath, "rb") as f:
			data = f.read()
			bucket.put_object(filepath , data)  # data can be a any file
			return "Upload Successfully"
	except:
		return "Upload correct file"

def download_file_alibaba(bucket_name,filepath):  # Download the file using file name and bucket name as parameter
	bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)
	try:
		ret=bucket.get_object_to_file(filepath, filepath) # file downloaded to current directory
	except:
		return 0
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
		return 'Not able to generate link'


def list_items_alibaba_bucket(bucket_name):  # list all the objects in the bucket using bucket name
	bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)
	objects_cloud=[]
	for obj in oss2.ObjectIterator(bucket):
		objects_cloud.append(obj.key)
	return objects_cloud

