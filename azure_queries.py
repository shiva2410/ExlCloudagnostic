import os
from azure.storage.blob import BlobServiceClient, BlobClient
from azure.storage.blob import ContentSettings, ContainerClient
from azure.storage.blob import generate_blob_sas
from azure.storage.blob import BlobSasPermissions
from datetime import datetime, timedelta
import pyshorteners
import yaml

# Open the file and load the file
def load_config():
    with open('config.yaml') as f:
        return yaml.load(f, Loader=yaml.FullLoader)

config = load_config()

MY_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName="+str(config["main_account_name"])+";AccountKey="+str(config["main_account_key"])+";EndpointSuffix=core.windows.net"
path = os.getcwd()
LOCAL_BLOB_PATH = str(path)+ "/download"

blob_service_client =  BlobServiceClient.from_connection_string(MY_CONNECTION_STRING)

def upload_file(MY_FILE_CONTAINER,localpath): # Function to upload files
    try:
        file_name = os.path.basename(localpath)
        blob_client = blob_service_client.get_blob_client(container=MY_FILE_CONTAINER, blob=file_name)
        
        with open(localpath, "rb") as data:
            blob_client.upload_blob(data,overwrite=True)
        return "File uploaded successfully"
    except:
        return "Something went wrong"

def download_file(MY_FILE_CONTAINER,blobname): # Function to download files for authorized users
    try:
        blob_client = blob_service_client.get_container_client(container= MY_FILE_CONTAINER)
        data = blob_client.get_blob_client(blobname).download_blob().readall()
        download_file_path = os.path.join(LOCAL_BLOB_PATH, blobname)
        with open(download_file_path, "wb") as file:
            file.write(data)
        return download_file_path
    except:
        return "Something went wrong"

def download_file_temp(MY_FILE_CONTAINER,blobname,expirytime): # Function to download files temporarily for unauthorized users
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
            type_tiny = pyshorteners.Shortener()
            short_url = type_tiny.tinyurl.short(url_with_sas)
            return short_url
        except:
            return url_with_sas
    except:
        return "Something went wrong"

def list_files(MY_FILE_CONTAINER): # Function to view files inside Container
    try:
        list_of_files=[]
        my_container = blob_service_client.get_container_client(container= MY_FILE_CONTAINER)
        my_blobs = my_container.list_blobs()
        for blob in my_blobs:
            list_of_files.append(blob.name)
        return list_of_files
    except:
        return "Something went wrong"

# print(upload_file('myfiles', LOCAL_FILE_PATH))
# print(download_file('myfiles', BLOB_FILE_NAME))
# print(list_files('exltrinity'))
# print(download_file_temp('myfiles', 'sample.jpeg',20))