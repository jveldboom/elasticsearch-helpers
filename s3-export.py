import sys, datetime
from subprocess import call

es_endpoint = raw_input("Elasticsearch Endpoint: ") or sys.exit('ERROR: Elasticsearch endpoint is required')
es_index = raw_input("Elastichsearch Index [all] ") or ""
backup_name = raw_input("Backup Name: ") or sys.exit('ERROR: Elasticsearch cluster name is required')
s3_bucket = raw_input("S3 Bucket Saving to: ") or sys.exit('ERROR: S3 Bucket is required')
aws_profile = raw_input("AWS Profile Name [default]: ") or "default"

date = datetime.datetime.today().strftime('%Y-%m-%d')

print "Pulling Latest Docker Image..."
call('docker pull taskrabbit/elasticsearch-dump',shell=True)

print "Dumping data from "+es_endpoint+"..."
call('docker run --rm -it -v $(pwd):/tmp taskrabbit/elasticsearch-dump \
  --input='+es_endpoint+'/'+es_index+' \
  --output=/tmp/'+backup_name+'-data-'+date+'.json \
  --type=data', shell=True)

print 'Dumping mappings from '+es_endpoint+'...'
call('docker run --rm -it -v $(pwd):/tmp taskrabbit/elasticsearch-dump \
  --input='+es_endpoint+'/'+es_index+' \
  --output=/tmp/'+backup_name+'-mapping-'+date+'.json \
  --type=mapping',shell=True)

print "Gzip snapshot JSON files..."
call('gzip '+backup_name+'*', shell=True)

print "Coping snapshot to S3..."
call('aws s3 cp $(pwd) s3://'+s3_bucket+' --recursive --exclude "*" --include "*.gz" --profile '+aws_profile, shell=True)

print "Cleaning up snapshot files..."
call('rm '+backup_name+'*.gz', shell=True)