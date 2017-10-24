FROM python:3
MAINTAINER nakkat

# configure environment
ENV SHELL /bin/bash
ENV WORK_DIR /usr/src/app

# set locale
ENV LANG C.UTF-8
RUN rm -f /etc/localtime
RUN ln -fs /usr/share/zoneinfo/Asia/Tokyo /etc/localtime
# ENV TZ Asia/Tokyo
# RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        gettext \
        vim \
        less \
        libmysqlclient-dev \
        libpq-dev \
        mysql-client \
        postgresql-client \
        sqlite3 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 --no-cache-dir install -U \
    mysqlclient \
    psycopg2 \
    django

VOLUME $WORK_DIR
WORKDIR $WORK_DIR

EXPOSE 8000

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
