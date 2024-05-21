FROM python:3.10.6 
LABEL maintainer Andy Chiou, IESDMC
# ARG USERNAME=dmc
# ARG UID=1000
# ARG GID=1000
ENV PYTHONUNBUFFERED=1

WORKDIR /code
COPY  web/requirements.txt /code/
RUN pip install -r requirements.txt\
    && apt-get update && apt-get install -y zip
# RUN pip install -r requirements.txt
# COPY . /code/ 

# RUN groupadd -g ${GID} ${USERNAME}
# RUN useradd -ms /bin/bash -g ${GID} -u ${UID} ${USERNAME}
# USER ${USERNAME}