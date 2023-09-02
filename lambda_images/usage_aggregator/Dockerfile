FROM public.ecr.aws/lambda/python:3.11

COPY . ${LAMBDA_TASK_ROOT}/

# INSTALL LAMBDA POWERTOOLS FOR LOOGING
RUN pip install aws-lambda-powertools

CMD [ "handler.lambda_handler" ]