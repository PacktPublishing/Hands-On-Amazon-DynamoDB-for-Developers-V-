Get All objects

sam package --s3-bucket colib-digitial-hands-on-dynamo --output-template-file packaged.yaml
sam deploy --template-file packaged.yaml --stack-name ttl-demo --capabilities CAPABILITY_IAM

aws cloudformation delete-stack --stack-name ttl-demo
