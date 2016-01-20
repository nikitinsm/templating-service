FROM pypy:2

RUN apt-get update && apt-get upgrade -y && \
    apt-get install git && \
    apt-get autoremove -y

COPY ./requirements.pip /srv/requirements.pip
RUN pip install -r /srv/requirements.pip

ENV APP_NAME="/templating"
ENV APP_ROOT="/opt${APP_NAME}"
ENV APP_REPOSITORY="${APP_ROOT}/repository"
ENV PYTHONPATH="${PYTHONPATH}:${APP_REPOSITORY}/src"

COPY . ${APP_REPOSITORY}

COPY ./docker/entrypoint.sh /bin/templating
RUN chmod 755 /bin/templating

EXPOSE 80

ENTRYPOINT ["templating"]