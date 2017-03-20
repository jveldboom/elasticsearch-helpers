# Elasticsearch Scripts

`s3-export.py` export data (whole cluster or individual indices) to S3  
`transfer-cluster.py` copies indices mapping and data to another cluster

## Requirements
- Docker (tested with Docker 1.13)
- Python

## Usages
List of ways to use these scripts

### s3-export.py
- Backup all indices or specific ones to S3. Could be setup to run on a cron schedule to have nightly backups
- Copy to S3 to import to another cluster

### transfer-cluster.py
- Transfer data, mappings, or both to another host or cluster
- Migrate data to new Elasticsearch version. (We used this to move from 2.3 to 5.1 on AWS)