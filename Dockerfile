FROM python:3.7
WORKDIR /app
RUN apt-get update -y
RUN apt-get install -y sqlite3 git-annex
RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - && apt-get install -y nodejs
RUN corepack enable
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
EXPOSE 4000

RUN flask db upgrade
RUN flask seed_test_db
RUN flask update_pipeline_data
RUN flask seed_test_experiments

CMD ["flask", "run", "--host", "0.0.0.0", "--port", "4000"]