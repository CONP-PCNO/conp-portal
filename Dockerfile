# syntax=docker/dockerfile:1
ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

RUN apt-get update -y
# RUN apt-get install --no-install-recommends -y \
RUN apt-get install -y \
    bash \
	acl \
	file \
	gettext \
	git \
    curl \
    rsync \
    unzip \
    sqlite3 \
    git-annex \
    datalad

# Install Node.js LTS and corepack
# RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - && apt-get install -y nodejs
# RUN corepack enable
# Get Node.js® v26.9.0 for. Linux using fnm with pnpm

RUN curl -o- https://fnm.vercel.app/install | bash -
RUN fnm install 26 && node -v
RUN npm install -g corepack
RUN corepack enable pnpm
RUN pnpm -v

RUN mkdir -p /root/.cache/boutiques/production/
COPY requirements-fixed.txt requirements.txt
COPY requirements-dev.txt requirements-dev.txt
RUN pip install -r requirements-dev.txt

COPY . .
EXPOSE 4000

COPY cli/docker-install.sh /docker-install.sh
RUN chmod +x /docker-install.sh
# RUN flask db upgrade
# RUN flask seed_test_db
# RUN flask update_pipeline_data
# RUN flask seed_test_experiments

# CMD ["flask", "run", "--host", "0.0.0.0", "--port", "4000"]
ENTRYPOINT ["/docker-install.sh"]
