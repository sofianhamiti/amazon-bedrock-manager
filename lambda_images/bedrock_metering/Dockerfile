FROM public.ecr.aws/lambda/python:3.11

COPY . ${LAMBDA_TASK_ROOT}/

# INSTALL PANDAS
RUN pip install pandas

CMD [ "handler.lambda_handler" ]