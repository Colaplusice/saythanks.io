FROM python:3.6
RUN adduser --disabled-login thanks_io
WORKDIR /home/thanks_io
COPY . .
RUN pip install -r requirements.txt -i https://pypi.doubanio.com/simple/
RUN chmod -R +x .
