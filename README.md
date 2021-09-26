# assets_history_producer_function

Producer function that triggers distributed consumer functions to fetch assets history

## To-do

### 1st run

- Trigger event from Gitlab w date example [01-09-2021]
- Rec payload via API
- Read payload in func
- Read asset details s3 path files
- Batch assets by 30
- Add 10 batch assets deplayed by incremental 90 secs
- Send to queue n0
- - iterate over available queues
- - need about 10 queues for 3000 assets

### 2nd run

- same with "failed"
- extract file names

### Wrap up

- Role out balance of region
- Deploy CICD pipeline

## Serverless cmd

```
serverless plugin install -n serverless-python-requirements --ENV_STAGE dev --AWS_REGION 'eu-west-1' --TARGET_S3_BUCKET 'dev.riskbloq.com' --TARGET_S3_ASSETS_DETAILS_PATH 'data/assets_details/latest/' --TARGET_S3_ASSETS_DETAILS_FILENAME 'assets_details_base.csv' --QUEUE_LIST_FILENAME 'queues.json' --TARGET_S3_ASSETS_HISTORY_LEAD_PATH 'data/assets_history/' --TARGET_S3_ASSETS_HISTORY_FAILED_TAIL_PATH '/failed/' --TARGET_S3_ASSETS_HISTORY_SUCCESSFUL_TAIL_PATH '/successful/'
```

```
serverless deploy --ENV_STAGE dev --AWS_REGION 'eu-west-1' --TARGET_S3_BUCKET 'dev.riskbloq.com' --TARGET_S3_ASSETS_DETAILS_PATH 'data/assets_details/latest/' --TARGET_S3_ASSETS_DETAILS_FILENAME 'assets_details_base.csv' --QUEUE_LIST_FILENAME 'queues.json' --TARGET_S3_ASSETS_HISTORY_LEAD_PATH 'data/assets_history/' --TARGET_S3_ASSETS_HISTORY_FAILED_TAIL_PATH '/failed/' --TARGET_S3_ASSETS_HISTORY_SUCCESSFUL_TAIL_PATH '/successful/'
```

```
serverless remove --ENV_STAGE dev --AWS_REGION 'eu-west-1' --TARGET_S3_BUCKET 'dev.riskbloq.com' --TARGET_S3_ASSETS_DETAILS_PATH 'data/assets_details/latest/' --TARGET_S3_ASSETS_DETAILS_FILENAME 'assets_details_base.csv' --QUEUE_LIST_FILENAME 'queues.json' --TARGET_S3_ASSETS_HISTORY_LEAD_PATH 'data/assets_history/' --TARGET_S3_ASSETS_HISTORY_FAILED_TAIL_PATH '/failed/' --TARGET_S3_ASSETS_HISTORY_SUCCESSFUL_TAIL_PATH '/successful/'
```
