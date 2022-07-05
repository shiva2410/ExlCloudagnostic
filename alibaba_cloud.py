import oss2
import os
import pyshorteners
access_key_id = 'LTAI5tMMRGbFNaHsoC16c2dc'
access_key_secret = 'kV8oIJaomxMSAmycOTbQiDTv59HliT'
bucket_name = 'exltrinity'
endpoint = 'oss-ap-south-1.aliyuncs.com' 
# Create Object for this bucket
bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)
# Upload the file using file name and bucket name as parameter
def upload(bucket_name,mainpath):
    head, filepath = os.path.split(mainpath)
    try:

        with open(filepath, "rb") as f:
            data = f.read()
            bucket.put_object(filepath , data)  # data can be a any file
            return "Upload Successfully"
    except:
        return "Upload correct file"
# Download the file using file name and bucket name as parameter
def download(bucket_name,filepath):
    try:
        ret=bucket.get_object_to_file(filepath, filepath) # file downloaded to current directory
    except:
        return 0
    return os.path.join(os.getcwd(),filepath) if ret.status==200 else 0 # returning path of current directory
# temporary downloading functionality using file name and bucket name as parameter
def download_temp(bucket_name,filepath):
    try:
        ret=bucket.get_object_to_file(filepath, filepath)
        ret_link = bucket.sign_url('GET', filepath,60)  # The return value is the link, the parameters are in order, method/file path on oss/expiration time(s) which is 60 sec
        type_tiny = pyshorteners.Shortener() #shortening link to protect data
        short_url = type_tiny.tinyurl.short(ret_link)
    except:
        return 0
    return short_url if ret.status==200 else 0

# list all the objects in the bucket using bucket name
def listall_objects(bucket_name):
    objects_cloud=[]
    for obj in oss2.ObjectIterator(bucket):
        objects_cloud.append(obj.key)
    return objects_cloud

mainpath="E:/chalkboard/cloud/upload.jpeg"
head, tail = os.path.split(mainpath)
# print(tail)
# print(upload(bucket_name,tail))
# print(download(bucket_name,tail))
# print(download_temp(bucket_name,tail))
# print(listall_objects(bucket_name))
