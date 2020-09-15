FROM vimagick/scrapyd:py3
MAINTAINER Murali Nallathiga<murali@digitaldots.ai>

WORKDIR /code

# update and upgrade to get the distutils
RUN set -xe \
    && apt-get update \
    && apt-get upgrade \
    && apt-get install -y python3.7-distutils

COPY . .
CMD chmod +x entrypoint.sh

EXPOSE 6800

RUN pip install -r requirements.txt

CMD ["scrapyd", "--pidfile="]
