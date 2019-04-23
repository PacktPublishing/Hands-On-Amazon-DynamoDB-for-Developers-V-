Get All objects

sam package --s3-bucket colib-digitial-hands-on-dynamo --output-template-file packaged.yaml
sam deploy --template-file packaged.yaml --stack-name pycharm-demo --capabilities CAPABILITY_IAM

```
aws dynamodb scan --table-name UsersTable

aws dynamodb scan \
     --table-name UsersTable \
     --filter-expression "first_name = :first_name" \
     --expression-attribute-values '{":first_name":{"S":"Dave"}}'
```
