FROM mcr.microsoft.com/devcontainers/typescript-node:1-22-bookworm

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends python3 python3-pip

# Symlink alias Python 3 and pip
RUN ln -s /usr/bin/python3 /usr/bin/python

RUN npm uninstall -g pnpm

WORKDIR /workspaces/frontend

ENV PNPM_HOME=/workspaces/pnpm
RUN corepack enable pnpm

COPY backend/requirements.txt /workspace/backend/

WORKDIR /workspace/backend

# Instead of using a Python venv, we're using a devcontainer for a similar purpose
RUN pip install -r requirements.txt --break-system-packages

RUN python -m pip install -U --upgrade-strategy only-if-needed aider-chat aider-chat[playwright] --break-system-packages

RUN echo 'alias pn=pnpm' >> /home/node/.bashrc
