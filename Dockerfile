FROM jupyterhub/jupyterhub:1.2
ENV SPAWNERDK_VERSION=0.11.1
ENV SPAWNERKB_VERSION=0.12.0 
ENV TZ=Europe/Paris

COPY  jupyterhub_config.py /srv/jupyterhub/jupyterhub_config.py

# Install dockerspawner
RUN apt-get update && apt-get -y install git libpq-dev tzdata && \
    pip install --no-cache-dir psycopg2-binary \
    dockerspawner==$SPAWNERDK_VERSION \
    jupyter_enterprise_gateway \
    jupyterhub-kubespawner==$SPAWNERKB_VERSION && \
    cd /home && \
    git clone -b dev https://github.com/jupyter-naas/nativeauthenticator.git && \
    cd nativeauthenticator && \
    pip install -e . 
