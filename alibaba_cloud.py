import oss2
import os
access_key_id = 'LTAI5tMMRGbFNaHsoC16c2dc'
access_key_secret = 'kV8oIJaomxMSAmycOTbQiDTv59HliT'
bucket_name = 'exltrinity'
endpoint = 'oss-ap-south-1.aliyuncs.com' 
# Create Object
bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)
# Upload 

def upload(bucket_name,mainpath):
    head, filepath = os.path.split(mainpath)
    try:

        with open(filepath, "rb") as f:
            data = f.read()
            bucket.put_object(filepath , data)  # data is data, it can be a picture
            ret = bucket.sign_url('GET', filepath,60*60*24)  # The return value is the link, the parameters are in order, method/file path on oss/expiration time(s)
            return ret
    except:
        return "Upload correct file"
def download(bucket_name,filepath):
    try:
        ret=bucket.get_object_to_file(filepath, filepath)
    except:
        return 0
    return 1 if ret.status==200 else 0
def listall_objects(bucket_name):
    objects_cloud=[]
    for obj in oss2.ObjectIterator(bucket):
        objects_cloud.append(obj.key)
    return objects_cloud

mainpath="E:/chalkboard/cloud/upload.jpeg"
head, tail = os.path.split(mainpath)
print(tail)
print(upload(bucket_name,tail))
print(download(bucket_name,tail))
print(listall_objects(bucket_name))