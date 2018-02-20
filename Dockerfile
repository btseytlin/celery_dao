FROM python:3.6-alpine

COPY requirements.txt /src/requirements.txt
RUN pip install -r /src/requirements.txt

ENV PYTHONPATH=/src

#COPY setup.py /src/setup.py
#RUN pip install --no-cache-dir -r /src/setup.py

COPY . /src
RUN python /src/setup.py develop

CMD ["celery_dao"]