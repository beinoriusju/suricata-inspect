FROM python:3.12

WORKDIR /app

COPY . /app
    
RUN pip install -r requirements.txt

EXPOSE 5000

ENV FLASK_SKIP_DOTENV=1

ENTRYPOINT ["python3", "-m", "flask", "run", "--host=0.0.0.0"]