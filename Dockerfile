FROM tiangolo/uwsgi-nginx-flask:python3.8
RUN apt update&& apt install -y bash vim git
ENV STATIC_URL /static
ENV STATIC_PATH /app/app/static
COPY ./requirements.txt /var/www/requirements.txt
RUN pip install -r /var/www/requirements.txt
