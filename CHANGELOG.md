## 2.8.0b4 (2020-12-11)

### Fix

- Remove changelog
- Path to launch kernel script

## 2.8.0b3 (2020-12-11)

### Fix

- Remove CHANGElog
- Move all kernelspecs into the container

## 2.8.0b2 (2020-12-11)

### Fix

- Remove changelog to fix CI
- Remove .DS_Store

### Feat

- Add kernels extra large
- Add size small/medium/large
- rename kernel
- Add resources request/limites
- Add affinity and toleration to kernel

## 2.8.0b1 (2020-11-24)

### Fix

- **ci**: retry without changelog
- **ci**: version in dockerfile
- fix typo
- readOnly: true had a typo

## 2.8.0b0 (2020-11-24)

### Feat

- Remove /usr/local/share/jupyter/kernels/python3

## 2.7.1 (2020-11-24)

### Fix

- make kernel mounted folder readOnly

## 2.7.0 (2020-11-24)

### Feat

- Update kernel.json and launch_kubernetes.py to use variables from singleuser

## 2.6.0 (2020-11-24)

### Feat

- add JUPYTER_SERVER_ROOT, JUPYTERHUB_USER and JUPYTERHUB_API_TOKEN

## 2.5.0 (2020-11-24)

### Feat

- Add environment variables to Kernel execution.

## 2.4.0 (2020-11-24)

### Feat

- Update launch_kubernetes.py to mount EFS volume for users

## 2.3.0 (2020-11-24)

### Feat

- Update kernel image used for enterprise-gateway

## 2.2.0 (2020-11-23)

### Feat

- add kernel folder

## 2.1.1 (2020-11-16)

## 2.1.0 (2020-11-09)

### Feat

- add new auth

### Fix

- :bug: fix hub version to 1.1.0
- :bug: use b64 font
- :bug: test 1.2 hub
- :bug: test version 1.1.0
- :bug: add missing naas logo
- :bug: use latest version of hub
