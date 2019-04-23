Get All objects

sam package --s3-bucket colib-digitial-hands-on-dynamo --output-template-file packaged.yaml
sam deploy --template-file packaged.yaml --stack-name pycharm-demo --capabilities CAPABILITY_IAM

aws cloudformation delete-stack --stack-name pycharm-demo\

```
aws dynamodb scan --table-name UsersTable

aws dynamodb scan \
     --table-name UsersTable \
     --filter-expression "last_login = : last_login" \
     --expression-attribute-values '{": last_login”:{“N”:1546519879010}}'

aws dynamodb scan \
     --table-name UsersTable \
     --filter-expression "last_login = :last_login" \
     --expression-attribute-values '{":last_login":{"N":"1546519879010"}}'
```
