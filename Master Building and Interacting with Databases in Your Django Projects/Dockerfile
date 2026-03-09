# it's a docker file

# user official python image 
FROM python:3.13.2-alpine3.21

# set working directory
WORKDIR /app

# copy project file
COPY requirements.txt requirements.txt

# install dependencies
RUN  pip install --no-cache-dir -r requirements.txt