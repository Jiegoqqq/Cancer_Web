FROM python:3.10

ENV PYTHONUNBUFFERED=1

RUN mkdir /winter_final
WORKDIR /winter_final
COPY . /winter_final/
RUN pip install -r requirements.txt
CMD ["python3","manage.py","runserver","0.0.0.0:8000"]