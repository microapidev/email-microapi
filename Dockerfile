FROM python:3

#environment variable to send application output to terminal without buffering
ENV PYTHONUNBUFFERED 1

#setting working directory and importing source code
RUN mkdir /code
WORKDIR /code
COPY . /code/

#getting requirements from Pipfile
RUN pip install pipenv
COPY Pipfile* /tmp/
RUN cd /tmp && pipenv lock --requirements > requirements.txt

#installing requirements
RUN pip install -r /tmp/requirements.txt
