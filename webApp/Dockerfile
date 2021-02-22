FROM python:3

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

#just for documentation, has no effect
EXPOSE 5000

CMD [ "python", "app.py" ]
