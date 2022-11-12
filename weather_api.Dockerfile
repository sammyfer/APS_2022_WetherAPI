FROM python:3.7

RUN mkdir /api
ADD weather-api.py /api

RUN pip3 install --default-timeout=300 requests fastapi uvicorn
CMD [ "uvicorn", "api.weather-api:app", "--reload" ]