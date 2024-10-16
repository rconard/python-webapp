FROM mcr.microsoft.com/devcontainers/typescript-node:1-22-bookworm AS base

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends python3 python3-pip

# Symlink alias Python 3 and pip
RUN ln -s /usr/bin/python3 /usr/bin/python

RUN npm uninstall -g pnpm

WORKDIR /workspace/frontend

ENV PNPM_HOME="/workspace/frontend/pnpm"
ENV PATH="$PNPM_HOME:$PATH"

# Install package-manager
# use corepack for easier installation
RUN corepack enable pnpm

# RUN pnpm config set store-dir /workspace/frontend/pnpm

# Install PM2
RUN pnpm install -g pm2

# Download dependencies from lockfile
# it's make build(local) faster because if there is no change in dependencies, it will use cache, 
# but with `package.json` It's updated frequently, so often it won't cache.)
# See more: https://pnpm.io/cli/fetch
COPY frontend/pnpm-lock.yaml /workspace/frontend/
RUN pnpm fetch

COPY frontend/package.json /workspace/frontend/
RUN pnpm install --offline
# RUN pnpm install
# RUN --mount=type=cache,id=pnpm,target=/workspace/frontend/pnpm/store pnpm install

# RUN --mount=type=cache,id=pnpm,target=/workspace/frontend/pnpm/store pnpm install --frozen-lockfile

# RUN pnpm run build









# ENV PNPM_HOME=/workspace/pnpm
# # RUN corepack enable && corepack install --global pnpm
# # ENV COREPACK_ENABLE_DOWNLOAD_PROMPT=0


# WORKDIR /workspace/frontend

# ENV PNPM_HOME=/workspace/pnpm

# # pnpm bug: https://github.com/pnpm/pnpm/issues/7050
# RUN pnpm config set store-dir /workspace/pnpm

# # pre-loads required packages from pnpm-lock.yaml into the store,
# # ready to be installed with `pnpm install`
# RUN pnpm fetch

# COPY frontend/package.json /workspace/frontend/
# RUN pnpm install --offline

COPY backend/requirements.txt /workspace/backend/

WORKDIR /workspace/backend

# Instead of using a Python venv, we're using a devcontainer for a similar purpose
RUN pip install -r requirements.txt --break-system-packages

RUN python -m pip install -U --upgrade-strategy only-if-needed aider-chat aider-chat[playwright] --break-system-packages
