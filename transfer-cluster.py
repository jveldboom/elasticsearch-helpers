import subprocess

host_input = raw_input("Source Elasticsearch Endpoint: ") or sys.exit('ERROR: Source Elasticsearch Endpoint is required')
host_output = raw_input("Destination Elasticsearch Endpoint: ") or sys.exit('ERROR: Destination Elasticsearch Endpoint is required')
es_index  = raw_input("Index to Copy [all]: ") or ""

# Uncomment to just hard code these values
# host_input='https://input.elasticsearch.domain:9200'
# host_output='https://output.elasticsearch.domain:9200'
# es_index='my-index-name'

print "Pulling Latest Docker Image..."
call('docker pull taskrabbit/elasticsearch-dump',shell=True)

# Get list of indices
output = subprocess.check_output("curl -s -XGET "+host_input+"/_cat/indices/"+es_index+" | awk '{print $3}' | sort", shell=True)

# Loop through list of indices
for index in output.splitlines():
	print "STARTING MAPPING: "+index
	subprocess.call("docker run --rm -i taskrabbit/elasticsearch-dump \
		--input="+host_input+"/"+index+" \
		--output="+host_output+"/"+index+" \
		--type=mapping", shell=True)

	print "STARTING DATA: "+index
	subprocess.call("docker run --rm -i taskrabbit/elasticsearch-dump \
		--input="+host_input+"/"+index+" \
		--output="+host_output+"/"+index+" \
		--type=data", shell=True)