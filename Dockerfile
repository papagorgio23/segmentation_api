###############################################
# Base Image
###############################################
FROM python:3.9 as python-base



###############################################
# Builder Image
###############################################
FROM python-base as builder-base
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    curl \
    build-essential


WORKDIR /src

COPY ./requirements.txt /src/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /src/requirements.txt


###############################################
# Production Image
###############################################
FROM python-base as production
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
COPY ./src /src/
COPY ./models /models/
COPY main.py /

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]