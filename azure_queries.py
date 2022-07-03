import os
from azure.storage.blob import BlobServiceClient, BlobClient
from azure.storage.blob import ContentSettings, ContainerClient
 
MY_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=exltrinity;AccountKey=JyH+zU96WW39aL2BeXk20MGj1f1hyeoEzT0qzDqeEVr0dGiqnewYfEOk/VUt01YWi/Yus81IHW+2+AStiKmUnA==;EndpointSuffix=core.windows.net"
 
MY_FILE_CONTAINER = "myfiles"

path = os.getcwd()
LOCAL_BLOB_PATH = str(path)+ "/download"

# LOCAL_FILE_PATH = str(path) + "/sample.jpeg"
# BLOB_FILE_NAME = "sample.jpeg"

blob_service_client =  BlobServiceClient.from_connection_string(MY_CONNECTION_STRING)

def upload_file(localpath):
    try:
        file_name = os.path.basename(localpath)
        blob_client = blob_service_client.get_blob_client(container=MY_FILE_CONTAINER, blob=file_name)
        
        with open(localpath, "rb") as data:
            blob_client.upload_blob(data,overwrite=True)
        return "File uploaded successfully"
    except:
        return "Something went wrong"

def download_file(blobname):
    try:
        blob_client = blob_service_client.get_container_client(container= MY_FILE_CONTAINER)
        data = blob_client.get_blob_client(blobname).download_blob().readall()
        download_file_path = os.path.join(LOCAL_BLOB_PATH, blobname)
        with open(download_file_path, "wb") as file:
            file.write(data)
        return download_file_path
    except:
        return "Something went wrong"

def list_files():
    try:
        list_of_files=[]
        my_container = blob_service_client.get_container_client(container= MY_FILE_CONTAINER)
        my_blobs = my_container.list_blobs()
        for blob in my_blobs:
            list_of_files.append(blob.name)
        return list_of_files
    except:
        return "Something went wrong"

# print(upload_file(LOCAL_FILE_PATH))
# print(download_file(BLOB_FILE_NAME))
# print(list_files())