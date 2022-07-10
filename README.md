# ExlCloudagnostic
### Exl Hackathon. Cloud Agnostic Solution
VIDEO PROTOTYPE LINK - https://youtu.be/jSO0XRCKrVg

Solution Document LINK - https://drive.google.com/file/d/1-FW4Y3JucmXXwyrvYhuNZVn85A7bCsvs/view?usp=sharing

## We have incorporated the following Cloud Providers in our solution:

1. AWS (Amazon Web Services): Millions of customers use AWS storage services to transform their business, increase agility, reduce costs, and accelerate innovation. Choose from a broad portfolio of
storage solutions with deep functionality for storing, accessing, protecting, and analyzing your data.
2. Microsoft Azure: The Azure Storage platform is Microsoft's cloud storage solution for modern data storage scenarios. Azure Storage offers highly available, massively scalable, durable, and secure storage for a variety of data objects in the cloud.
3. Alibaba Cloud: Alibaba Cloud Object Storage Service (OSS) provides industry-leading scalability, durability and performance. Customers of all sizes and industries can use it to store and protect any amount of data for use cases, such as backup and restore, content
distribution, data lakes, websites, mobile applications ,data archive and IoT devices.

## Appropriate handling of sensitive keys and information for all Cloud Platforms:

- To setup AWS credentials, run the following commands: 
  - Firstly, install AWS CLI.
    - curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg" sudo installer -pkg AWSCLIV2.pkg -target /
  - Run the following command for AWS configuration 
    - aws configure
  - Enter your AWS credentials and make sure it has access to AWS S3.
- To setup AZURE credentials, run the following commands: 
  - Setup environment variables
    - export azure_account_name="<account-name>"
    - export azure_account_key="<account-key>"
- To setup ALIBABA credentials, run the following commands: 
  - Setup environment variables
    - export alibaba_access_key_id="<access-key-id>"
    - export alibaba_access_key_secret="<access-key-secret>"

## Functionality of our Cloud-agnostic solution:

1. Upload Feature: The authorized user can upload files (such as jpg, pdf, doc, ppt etc) to any desired cloud platform.
2. Download Feature: The authorized user can download any file from the cloud platforms directly by providing the filename.
3. Download Temporary Feature: The unauthorized user will receive a temporary link which will be valid to download a particular file for a given amount of time. Also, for security purposes we have created short URL using python library “pyshorteners” because the link generated by the cloud SDKs were displaying credentials inside the link.
4. List the Files Feature: To make it easy for the authorized user to know which files are available in the cloud storages, this feature will allow authorized users to view all the files in the selected cloud platform.
5. Delete Feature: This is again an added functionality of our solution which enhances the user experience by allowing an authorized user to delete a file from the selected cloud storage.


## Steps to execute the code:

- Make sure your working directory is same as the code directory and Python 3 is installed in the system.
- To install all the packages and dependencies required, run the following command: a. “pip install -r requirements.txt”
- Now to start the application, run the following command:
  - “python3 app.py”
