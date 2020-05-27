# UDEND-P3
## PROJECT 1
### ETL using Amazon Redshift

**Sparkify is a music streaming startup , they have been collecting data about user activity on their system.**
**Sparkify analytics team is trying to understand more about what users are listening to**

Fact & Dimensions Table:

![alt text](https://app.lucidchart.com/publicSegments/view/13584d37-ae3c-4049-82a0-1c3a3fc68a6d/image.png)


#### DATASETS hosted in S3:
* Subset of [Million Song Dataset](http://millionsongdataset.com/)
* Logdata generated by an [Event Log Simulator](https://github.com/Interana/eventsim)

#### Files included in the REPO:
- Infra Folder  :
1. USES Terraform to automate creating and destroying a 4 node Redshift cluster in AWS
#### STEPS TO deploy using Terraform [Optional]:
1. Install Terraform by downloading exe and adding it to Path (https://www.terraform.io/downloads.html)
2. Create a terraform.tfvars with following format and add your AWS KEY ID and secret details as well as redshift admin and password accounts make sure it gets execluded in .gitignore file
``` code
# AWS KEY & SECRET
AWS_KEY_ID = ""
AWS_SECRET = ""
# REDSHIFT admin & pass
RSHIFT_USER = ""
RSHIFT_PASS = ""
```
3. run terraform apply -auto-approve
4. After terraform runs successfully you will see the following outputs

``` code
Outputs:

role_arn = arn:aws:iam::XXXXXXX/redshift_role
rs_endpoint = sparkify-cluster.XXXXXX.us-west-2.redshift.amazonaws.com:5439

```
The outputs can then be used in the dwh.cfg which should be created in the root of the cloned repo. with the following format:
``` code
[CLUSTER]
HOST='sparkify-cluster.XXXXX.us-west-2.redshift.amazonaws.com'
DB_NAME='sparkify'
DB_USER=''
DB_PASSWORD=''
DB_PORT=5439

[IAM_ROLE]
ARN='arn:aws:iam::XXXXX:role/redshift_role'

[S3]
LOG_DATA='s3://udacity-dend/log_data'
LOG_JSONPATH='s3://udacity-dend/log_json_path.json'
SONG_DATA='s3://udacity-dend/song_data'
```
- sql_queries python script that contains the DB create & insert statements sepearted in their own file for modularity 
- create_tables.py python file that automatically drops the tables if they already exists and creates the tables as defined in the SQL Queries
- etl python script that contains the main program and manages the file processing needed for reading the files in JSON formats from the S3 Buckets and inserting the data to the DB tables that was defined by the create_tables.py script
#### STEPS TO RUN PROJECT:
1. RUN create_tables.py file to create all DB tables
2. RUN etl.py file to insert all records in the tables


