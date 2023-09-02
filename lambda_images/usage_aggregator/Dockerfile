FROM public.ecr.aws/lambda/python:3.11

COPY . ${LAMBDA_TASK_ROOT}/

# INSTALL LAMBDA POWERTOOLS FOR LOOGING
RUN pip install tiktoken==0.4.0

CMD [ "handler.lambda_handler" ]