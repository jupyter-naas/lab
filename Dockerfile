FROM jupyterhub/jupyterhub:1.3
ENV TZ=Europe/Paris

COPY  jupyterhub_config.py /srv/jupyterhub/jupyterhub_config.py

COPY naas_logo.svg /srv/jupyterhub/naas_logo.svg
COPY naas_fav.svg /srv/jupyterhub/naas_fav.svg
COPY requirements.txt /tmp/requirements.txt

# Install dockerspawner
RUN apt-get update && apt-get -y install git libpq-dev tzdata && \
    pip install --no-cache-dir -r /tmp/requirements.txt && \
    cd /home && \
    git clone https://github.com/jupyter-naas/authenticator.git && \
    cd authenticator && \
    pip install -e . 
