#!/usr/bin/python3
import boto3
import uuid
import logging

s3_client = boto3.client('s3')
s3_resource=boto3.resource('s3')

#create anme for bucket
def create_bucket_name(bucket_prefix):
    # The generated bucket name must be between 3 and 63 chars long
    return ''.join([bucket_prefix, str(uuid.uuid4())])

def create_bucket(bucket_prefix, s3_connection):
       session = boto3.session.Session()
       current_region = session.region_name
       bucket_name = create_bucket_name(bucket_prefix)
       bucket_response = s3_connection.create_bucket(Bucket=bucket_name,CreateBucketConfiguration={'LocationConstraint': current_region})
       print(bucket_name, current_region)
       return bucket_name, bucket_response


   #creat bucket with client
first_bucket_name,first_response = create_bucket( bucket_prefix='firstpythonbucket',s3_connection=s3_resource.meta.client)


  #creat bucket with resource
second_bucket_name, second_response = create_bucket(bucket_prefix='secondpythonbucket',s3_connection=s3_resource)

#create file

def create_temp_file(size, file_name, file_content):
      random_file_name = ''.join([str(uuid.uuid4().hex[:6]), file_name])
      with open(random_file_name, 'w') as f:
        f.write(str(file_content) * size)
      return random_file_name

first_file_name = create_temp_file(300, 'firstfile.txt', 'f') 

first_bucket = s3_resource.Bucket(name=first_bucket_name)
first_object = s3_resource.Object(bucket_name=first_bucket_name, key=first_file_name)
first_object_again = first_bucket.Object(first_file_name)
first_bucket_again = first_object

#uploading file  object instance version

s3_resource.Object(first_bucket_name, first_file_name).upload_file(Filename=first_file_name)

#or via first_object instance
first_object.upload_file(first_file_name)

#uploading file Bucket Instance Version

s3_resource.Bucket(first_bucket_name).upload_file(Filename=first_file_name, Key=first_file_name)


#uploading file Client Instance Version
s3_resource.meta.client.upload_file(Filename=first_file_name, Bucket=first_bucket_name,Key=first_file_name) 

#downloads file
s3_resource.Object(first_bucket_name, first_file_name).download_file(f'/tmp/{first_file_name}') # Python 3.6+

#copying object between buckets

def copy_to_bucket(bucket_from_name, bucket_to_name, file_name):
    copy_source = {
        'Bucket': bucket_from_name,
        'Key': file_name
    }
    s3_resource.Object(bucket_to_name, file_name).copy(copy_source)

copy_to_bucket(first_bucket_name, second_bucket_name, first_file_name)

# delete an object

#s3_resource.Object(second_bucket_name, first_file_name).delete()

#ACL (Access Control Lists)
second_file_name = create_temp_file(400, 'secondfile.txt', 's')
second_object = s3_resource.Object(first_bucket.name, second_file_name)
second_object.upload_file(second_file_name, ExtraArgs={ 'ACL': 'public-read'})
second_object_acl = second_object.Acl()
print( second_object_acl.grants)
#Access control change
print( second_object_acl.put(ACL='private'))

#encryption

third_file_name = create_temp_file(300, 'thirdfile.txt', 't')
third_object = s3_resource.Object(first_bucket_name, third_file_name)
third_object.upload_file(third_file_name, ExtraArgs={'ServerSideEncryption': 'AES256'})

#data

#STANDARD: default for frequently accessed data
#STANDARD_IA: for infrequently used data that needs to be retrieved rapidly when requested
#ONEZONE_IA: for the same use case as STANDARD_IA, but stores the data in one Availability Zone instead of three
#REDUCED_REDUNDANCY: for frequently used noncritical data that is easily 

third_object.upload_file(third_file_name, ExtraArgs={'ServerSideEncryption': 'AES256', 'StorageClass': 'STANDARD_IA'})

#reload changes

third_object.reload()


#enable file versions

def enable_bucket_versioning(bucket_name):
    bkt_versioning = s3_resource.BucketVersioning(bucket_name)
    bkt_versioning.enable()
    print(bkt_versioning.status)

enable_bucket_versioning(first_bucket_name)

#2 versions of first file 
s3_resource.Object(first_bucket_name, first_file_name).upload_file(first_file_name)
s3_resource.Object(first_bucket_name, first_file_name).upload_file(third_file_name)
#latest version of the file
s3_resource.Object(first_bucket_name, first_file_name).version_id

#TRAVERSAL

#bucket
for bucket in s3_resource.buckets.all():
       print(bucket.name)

#objects
for obj in first_bucket.objects.all():
      print(obj.key )     
