FROM python:3.10.13-bookworm as builder
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host mirrors.tuna.tsinghua.edu.cn poetry
WORKDIR /opt/lawen
COPY . /opt/lawen
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --all-extras
