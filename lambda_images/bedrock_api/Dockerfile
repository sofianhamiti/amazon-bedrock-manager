FROM public.ecr.aws/lambda/python:3.11

COPY . ${LAMBDA_TASK_ROOT}/

# INSTALL BEDROCK SDK AND LANGCHAIN
RUN pip install sdk/boto3-1.26.142-py3-none-any.whl
RUN pip install sdk/botocore-1.29.142-py3-none-any.whl

CMD [ "handler.lambda_handler" ]