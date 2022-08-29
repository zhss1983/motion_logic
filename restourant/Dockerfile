FROM python:3.10.6
RUN mkdir /code
COPY requirements.txt /code
RUN pip install --upgrade pip && pip3 install -r /code/requirements.txt
COPY . /code
WORKDIR /code
#RUN python3 manage.py makemigrations && python3 manage.py migrate
CMD gunicorn restourant.wsgi:application --bind 0.0.0.0:8000
