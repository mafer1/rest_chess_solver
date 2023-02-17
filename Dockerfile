FROM python:3.8.16-alpine
WORKDIR /src

COPY . .

RUN python -m pip install -r requirements.txt

ENV FLASK_APP=app.py
WORKDIR /src/project

EXPOSE 8000
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "-p", "8000"]
