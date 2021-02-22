FROM python:3

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . ./ShoppingListApp

#just for documentation, has no effect
EXPOSE 5000

CMD [ "flask", "run", "--host=0.0.0.0"]
