FROM public.ecr.aws/lambda/python:3.11

COPY . ${LAMBDA_TASK_ROOT}/

# INSTALL BOTO3 WITH BEDROCK SDK
RUN pip install boto3==1.28.57

# INSTALL LAMBDA POWERTOOLS FOR LOOGING
RUN pip install aws-lambda-powertools==2.23.1

CMD [ "handler.lambda_handler" ]