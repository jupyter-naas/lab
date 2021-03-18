FROM jupyterhub/jupyterhub:1.2
ENV SPAWNERDK_VERSION=0.11.1
ENV HUB_VERSION=1.1.0
ENV SPAWNERKB_VERSION=0.12.0 
ENV TZ=Europe/Paris
ENV LAB_VERSION=2.0.0
ENV AUTH_VERSION=0.3.50

COPY  jupyterhub_config.py /srv/jupyterhub/jupyterhub_config.py

COPY naas_logo.svg /srv/jupyterhub/naas_logo.svg
COPY naas_fav.svg /srv/jupyterhub/naas_fav.svg

# Install dockerspawner
RUN apt-get update && apt-get -y install git libpq-dev tzdata && \
    pip install --use-feature=2020-resolver --no-cache-dir psycopg2-binary \
    dockerspawner==$SPAWNERDK_VERSION \
    jupyterhub==$HUB_VERSION \
    jupyter_enterprise_gateway \
    jupyterhub-kubespawner==$SPAWNERKB_VERSION && \
    cd /home && \
    git clone -b $AUTH_VERSION --depth 1 https://github.com/jupyter-naas/authenticator.git && \
    cd authenticator && \
    pip install -e . 

# Kernelspec for enterprise-gateway
COPY ./kernelspecs/python_kubernetes /usr/local/share/jupyter/kernels/python_kubernetes
