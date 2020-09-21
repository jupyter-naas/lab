# Copyright (c) Naas Development Team.
# Distributed under the terms of the Modified BSD License.

import os

c = get_config()

c.NotebookApp.ResourceUseDisplay.track_cpu_percent = True
c.NotebookApp.ResourceUseDisplay.mem_warning_threshold = 0.1
c.NotebookApp.ResourceUseDisplay.cpu_warning_threshold = 0.1

# We rely on environment variables to configure JupyterHub so that we
# avoid having to rebuild the JupyterHub container every time we change a
# configuration parameter.

# Spawn single-user servers as Docker containers
c.JupyterHub.spawner_class = 'kubespawner.KubeSpawner'
c.JupyterHub.service_tokens = {
    'secret-token': os.environ.get('ADMIN_API_TOKEN', 'SHOULD_BE_CHANGED'),
}

c.KubeSpawner.image = os.environ['DOCKER_NOTEBOOK_IMAGE']
c.KubeSpawner.image_pull_policy = 'Always'

# JupyterHub requires a single-user instance of the Notebook server, so we
# default to using the `start-singleuser.sh` script included in the
# jupyter/docker-stacks *-notebook images as the Docker run command when
# spawning containers.  Optionally, you can override the Docker run command
# using the DOCKER_SPAWN_CMD environment variable.
c.KubeSpawner.environment = {
    'JUPYTERHUB_URL': os.environ.get('JUPYTERHUB_URL', ''),
    'PUBLIC_DK_API': os.environ.get('PUBLIC_DK_API', ''),
    'TC_API_SCREENSHOT': os.environ.get('TC_API_SCREENSHOT', ''),
    'ALLOWED_IFRAME': os.environ.get('ALLOWED_IFRAME', ''),
    'TZ': os.environ.get('TZ', 'Europe/Paris')
}

c.KubeSpawner.cpu_guarantee = os.environ.get('KUBE_CPU_GUAR', 0.3)
c.KubeSpawner.cpu_limit = os.environ.get('KUBE_CPU_LIMIT', 1.0)
c.KubeSpawner.mem_limit = os.environ.get('KUBE_MEM_LIMIT', '4G')
c.KubeSpawner.mem_guarantee = os.environ.get('KUBE_MEM_GUAR', '500M')

# Explicitly set notebook directory because we'll be mounting a host volume to
# it.  Most jupyter/docker-stacks *-notebook images run the Notebook server as
# user `jovyan`, and set the notebook directory to `/home/jovyan/work`.
# We follow the same convention.
notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/ftp'
c.KubeSpawner.notebook_dir = notebook_dir
# Mount the real user's Docker volume on the host to the notebook user's

c.KubeSpawner.volumes = [
    {
        'name': 'nfs-root',
        'nfs': {
            'server': os.environ.get('VOLUME_SERVER', 'fs-b87bd009.efs.eu-west-3.amazonaws.com'),
            'path': '/'
        }
    }
]

c.KubeSpawner.volume_mounts = [
    {
        'name': 'nfs-root',
        'mountPath': os.environ.get('DOCKER_NOTEBOOK_DIR'),
        'subPath':  os.environ.get('KUBE_NAMESPACE', 'prod') + '/ftpusers/{username}'
    }
]

# This is used to set proper rights on NFS mount point.
c.KubeSpawner.lifecycle_hooks = {
    "postStart": {
        "exec": {
            "command": ["/bin/sh", "-c", f"chown -R 21:21 {os.environ.get('DOCKER_NOTEBOOK_DIR')}"]
        }
    }
}


c.KubeSpawner.extra_pod_config = {
    "subdomain": "jupyter-single-user",
    "hostname": "jupyter-{username}",
    "affinity": {
        "nodeAffinity": {
        "requiredDuringSchedulingIgnoredDuringExecution": {
            "nodeSelectorTerms": [
            {
                "matchExpressions": [
                {
                    "key": "jupyterNodeGroup",
                    "operator": "In",
                    "values": [
                    "true"
                    ]
                }
                ]
            }
            ]
        }
        }
    },
    "tolerations": [
        {
        "key": "jupyter",
        "operator": "Equal",
        "value": "true",
        "effect": "NoSchedule"
        }
    ]
}

c.KubeSpawner.extra_labels = {
    "name": "jupyter-single-user"
}
# For debugging arguments passed to spawned containers
c.KubeSpawner.debug = True
c.KubeSpawner.start_timeout = 120

# User containers will access hub by container name on the Docker network
c.JupyterHub.hub_ip = os.environ.get('HOST', '0.0.0.0')
c.JupyterHub.hub_port = os.environ.get('PORT', 8081)

c.KubeSpawner.hub_connect_ip = 'hub'

# Authenticate users with local
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