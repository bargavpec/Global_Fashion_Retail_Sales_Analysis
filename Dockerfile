# First-time build can take upto 10 mins.

FROM apache/airflow:2.10.4

ENV AIRFLOW_HOME=/opt/airflow

USER root
RUN apt-get update && \
    apt-get install -y openjdk-17-jdk unzip && \
    apt-get clean

# Set JAVA_HOME
ENV JAVA_HOME /usr/lib/jvm/java-17-openjdk-amd64/
ENV PATH="${JAVA_HOME}/bin:${PATH}"
RUN export JAVA_HOME

USER $AIRFLOW_UID
#RUN apt-get update -qq && apt-get install vim -qqq
# git gcc g++ -qqq

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install apache-airflow-providers-apache-spark


# Ref: https://airflow.apache.org/docs/docker-stack/recipes.html

SHELL ["/bin/bash", "-o", "pipefail", "-e", "-u", "-x", "-c"]

USER root
ARG CLOUD_SDK_VERSION=452.0.1
ENV GCLOUD_HOME=/home/google-cloud-sdk
#ENV CLOUDSDK_PYTHON=$(which python3.11)

ENV PATH="${GCLOUD_HOME}/bin/:${PATH}"

RUN DOWNLOAD_URL="https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-${CLOUD_SDK_VERSION}-linux-x86_64.tar.gz" \
    && TMP_DIR="$(mktemp -d)" \
    && curl -fL "${DOWNLOAD_URL}" --output "${TMP_DIR}/google-cloud-sdk.tar.gz" \
    && mkdir -p "${GCLOUD_HOME}" \
    && tar xzf "${TMP_DIR}/google-cloud-sdk.tar.gz" -C "${GCLOUD_HOME}" --strip-components=1 \
    && "${GCLOUD_HOME}/install.sh" \
       --bash-completion=false \
       --path-update=false \
       --usage-reporting=false \
       --quiet \
    && rm -rf "${TMP_DIR}" \
    && gcloud --version

WORKDIR $AIRFLOW_HOME

COPY scripts scripts
RUN chmod +x scripts

USER $AIRFLOW_UID