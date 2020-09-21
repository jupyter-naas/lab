# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# Configuration file for JupyterHub
import os

c = get_config()

# We rely on environment variables to configure JupyterHub so that we
# avoid having to rebuild the JupyterHub container every time we change a
# configuration parameter.

# Spawn single-user servers as Docker containers
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
c.JupyterHub.service_tokens = {
    'secret-token': os.environ.get('ADMIN_API_TOKEN', 'SHOULD_BE_CHANGED'),
}
# Spawn containers from this image
c.DockerSpawner.image = os.environ['DOCKER_NOTEBOOK_IMAGE']
c.DockerSpawner.pull_policy = 'always'

# JupyterHub requires a single-user instance of the Notebook server, so we
# default to using the `start-singleuser.sh` script included in the
# jupyter/docker-stacks *-notebook images as the Docker run command when
# spawning containers.  Optionally, you can override the Docker run command
# using the DOCKER_SPAWN_CMD environment variable.
c.DockerSpawner.environment = {
    'PUBLIC_DATASCIENCE': os.environ.get('PUBLIC_DATASCIENCE', ''),
    'DK_API': os.environ.get('DK_API', ''),
    'DK_API_PREPROD': os.environ.get('DK_API_PREPROD', ''),
    'PUBLIC_DK_API': os.environ.get('PUBLIC_DK_API', ''),
    'PUBLIC_DK_API_PREPROD': os.environ.get('PUBLIC_DK_API_PREPROD', ''),
    'HC_API': os.environ.get('HC_API', ''),
    'TC_API_SCREENSHOT': os.environ.get('TC_API_SCREENSHOT', ''),
    'ALLOWED_IFRAME': os.environ.get('ALLOWED_IFRAME', ''),
    'TZ': 'Europe/Paris',
}
spawn_cmd = os.environ.get('DOCKER_SPAWN_CMD', 'start-singleuser.sh')
c.DockerSpawner.extra_create_kwargs.update({'command': spawn_cmd})
# Connect containers to this Docker network
network_name = os.environ['DOCKER_NETWORK_NAME']
c.DockerSpawner.use_internal_ip = True
c.Spawner.mem_limit = '4G'
c.DockerSpawner.network_name = network_name
# Pass the network name as argument to spawned containers
c.DockerSpawner.extra_host_config = {'network_mode': network_name}
# Explicitly set notebook directory because we'll be mounting a host volume to
# it.  Most jupyter/docker-stacks *-notebook images run the Notebook server as
# user `jovyan`, and set the notebook directory to `/home/jovyan/work`.
# We follow the same convention.
notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/ftp/ftp'
c.DockerSpawner.notebook_dir = notebook_dir
# Mount the real user's Docker volume on the host to the notebook user's
# notebook directory in the container
c.DockerSpawner.volumes = {
    '/app/ftp/{username}': {"bind": notebook_dir, "mode": "z"},
}
# Remove containers once they are stopped
c.DockerSpawner.remove_containers = True
# For debugging arguments passed to spawned containers
c.DockerSpawner.debug = True

# User containers will access hub by container name on the Docker network
c.JupyterHub.hub_ip = os.environ.get('HOST', '0.0.0.0')
c.JupyterHub.hub_port = os.environ.get('PORT', 8080)

# Authenticate testing module, you need to comment GitHub OAuth to use it
#c.JupyterHub.authenticator_class = 'dummyauthenticator.DummyAuthenticator'

# Authenticate users with GitHub OAuth
c.JupyterHub.authenticator_class = 'nativeauthenticator.NativeAuthenticator'
c.Authenticator.check_common_password = True
c.Authenticator.minimum_password_length = 10

# Persist hub data on volume mounted inside container
data_dir = os.environ.get('DATA_VOLUME_CONTAINER', '/data')

c.JupyterHub.cookie_secret_file = os.path.join(data_dir,
                                               'jupyterhub_cookie_secret')

c.JupyterHub.db_url = 'postgresql://postgres:{password}@{host}/{db}'.format(
    host=os.environ['POSTGRES_HOST'],
    password=os.environ['POSTGRES_PASSWORD'],
    db=os.environ['POSTGRES_DB'],
)

c.JupyterHub.tornado_settings = {
    'headers': {
        'Content-Security-Policy': 'frame-ancestors self ' + os.environ.get('ALLOWED_IFRAME', '')
    }
}

# Whitlelist users and admins
c.Authenticator.whitelist = whitelist = set()
c.Authenticator.admin_users = admin = set()
c.JupyterHub.admin_access = True
