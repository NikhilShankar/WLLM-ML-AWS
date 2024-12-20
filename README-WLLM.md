create venv for py 3.11
```py -3.11 -m venv wllm-venv```

install pip dependencis
```pip install -r wllm-min-requirements.txt```


### Since we are on windows and aws lambda works on linux we need to create dependecies for linux. Hence we will use dcker to set this up correctly.
docker run -it --rm --entrypoint /bin/bash public.ecr.aws/lambda/python:3.11



### Lambda doesn't use venv directly, so you must package the dependencies with your Lambda function:
- Install to a Specific Directory: Install libraries into the hello_world/ directory:
- ```pip install -r requirements.txt -t hello_world/```
> This places all required libraries alongside your Lambda code.

### After adding dependencies, you can test the Lambda function locally using AWS SAM CLI:

Run Local Tests:
```sam build``` - this creates the .aws-sam folder which is used for deployment
```sam local invoke WLLMCosinePredictionHelper --event events/event.json```