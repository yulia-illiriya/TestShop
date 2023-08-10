FROM python:3.9.13

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8000

WORKDIR /

COPY requirements.txt /

RUN pip install --no-cache-dir -r requirements.txt

COPY . /

CMD ["python", "manage.py", "runserver"]