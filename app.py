from flask import Flask,abort,render_template,request,redirect,url_for,send_from_directory,Response
import os
import utils
import json
from flask_cors import CORS
import logging
app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)  #Setup logging level in the Flask APP 
@app.route('/cloudagnostic/',methods = ['POST'])
def cloud_agnostic():
	cloud_provider=request.form.get('cloud_provider')
	accesstype=request.form.get('accesstype')
	featuretype=request.form.get('featuretype')
	bucket_name=request.form.get('bucket_name')
	try:
		if featuretype=='upload' and accesstype=="authorized":        # feature type for uploading files in the respective cloud buckets
			try:
				if 'ufile' not in request.files:
					return 'No file part'
				file = request.files['ufile']
				if file:
					filename = file.filename
					# location=UPLOAD_FOLDER+'/'+filename
					# file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
					location=filename
					file.save(location)
					print(location)
				if cloud_provider=='aws':
					print(utils.upload_file_aws(bucket_name,location))
				elif cloud_provider=='azure':
					utils.upload_file_azure(bucket_name,location)
				elif cloud_provider=='alibaba':
					utils.upload_file_alibaba(bucket_name,location)
				return 'File uploaded successfully', 200
			except:
				return 'Error occured', 501

		elif featuretype=='download' and accesstype=="authorized":  # feature type for downloading files from the respective cloud buckets
			try:
				filename_download=request.form.get('file_download')
				if cloud_provider=='aws':
					file_path=utils.download_file_aws(bucket_name,filename_download)
				elif cloud_provider=='azure':
					file_path=utils.download_file_azure(bucket_name,filename_download)
				elif cloud_provider=='alibaba':
					file_path=utils.download_file_alibaba(bucket_name,filename_download)
				print(file_path,"--------")
				if file_path=='No such object found':
					return Response('File or Bucket does not exist', 404)
				print("here")
				path_d=os.getcwd()
				return send_from_directory(path_d, filename_download, as_attachment=True), 200
			except Exception as e:
				print(e)
				return 'Error occured', 501

		elif featuretype=='download' and accesstype=="unauthorized":  # feature type for creating temporary download link of files present in the respective cloud buckets
			try:
				expiration_time=int(request.form.get('exptime'))
				filename_download=request.form.get('file_download')
				if cloud_provider=='aws':
					file_url=utils.download_file_temp_aws(bucket_name,filename_download,expiration_time)
				elif cloud_provider=='azure':
					file_url=utils.download_file_temp_azure(bucket_name,filename_download,expiration_time)
				elif cloud_provider=='alibaba':
					file_url=utils.download_file_temp_alibaba(bucket_name,filename_download,expiration_time)
				else:
					print("Something wrong", file_url)
				if file_url=='No such object found':
					return Response('File or Bucket does not exist', 404)
				return file_url
			except:
				return 'Error occured', 501

		elif featuretype=='listfiles' and accesstype=="authorized": # feature type for listing files present in the respective cloud buckets
			try:
				if cloud_provider=='aws':
					listoffiles= utils.list_items_aws_bucket(bucket_name)
				elif cloud_provider=='azure':
					listoffiles= utils.list_items_azure_bucket(bucket_name)
				elif cloud_provider=='alibaba':
					listoffiles= utils.list_items_alibaba_bucket(bucket_name)
				print(listoffiles)
				list_files=[]
				for i in range(len(listoffiles)):
					dictoffiles={}
					dictoffiles['SrNo']=i+1
					dictoffiles['FileName']=listoffiles[i]
					list_files.append(dictoffiles)
				print(list_files)
				json_list=json.dumps(list_files)
				return json_list
			except:
				return 'Error occured', 501
		else:
			return 'Select right option or check your authentication type'
	except:
		return 'Error occured', 502

if __name__ == '__main__':
	app.run(debug = True,host='0.0.0.0', port=5200)