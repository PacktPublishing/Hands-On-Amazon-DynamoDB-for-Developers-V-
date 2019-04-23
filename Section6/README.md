sam package --s3-bucket colib-digitial-hands-on-dynamo --output-template-file packaged.yaml
sam deploy --template-file packaged.yaml --stack-name stream-demo --capabilities CAPABILITY_IAM

aws cloudformation delete-stack --stack-name stream-demo

```
CREATE DATABASE hands_on_dynamo

CREATE EXTERNAL TABLE user_table (
  create_time double,
  user_id string,
  email_address string,
  first_name string,
  last_name string,
  last_login double
) 
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde' 
WITH SERDEPROPERTIES ("separatorChar" = ",", "escapeChar" = "\\") 
LOCATION 's3://stream-demo-colibriusersinkbucket-165jl2f853m7u/'
TBLPROPERTIES ("skip.header.line.count"="1");

select count(*), max(create_time), avg(create_time) from user_table;
```
