# Fruit freshness detector web app 2024

Our website can predict the level of ripeness of fruits and recommend that you should eat or not.

## Prerequisite

- Python 3

## Setup

Clone this repository and go to the cloned folder.
```bash
git clone https://github.com/PyaeLinn01/fruit-freshness-detector.git
cd fruit-freshness-detector
```


Create python virtual environment.
```bash
pip install virtualenv
virtualenv venv
```

Initialize virtual environment
```bash
source venv/bin/activate
```
or use this if you are using windows
```
.\venv\bin\activate
```


Install dependencies using [pip](https://pip.pypa.io/en/stable/).
```bash
pip install -r requirements.txt
```

run the app with Flask
```bash
flask run
```

and lastly, open http://127.0.0.1:5000/ on your browser.

## Deployment

### Deploy to Heroku
```bash
heroku login
heroku git:clone -a fruit-freshness-detector-web
cd fruit-freshness-detector-web
git add .
git commit -am "make it better"
git push heroku master
```

### Deploy to Google App Engine
```bash
gcloud app deploy
```

### Deploy to Google Cloud Run
```bash
gcloud builds submit --tag gcr.io/PROJECT-ID/fruit-freshness-detector-web
gcloud run deploy --image gcr.io/PROJECT-ID/fruit-freshness-detector-web  
```

## API

### Recognize Image

----

  Return recognize result as JSON.

* **URL**

  /api/recognize

* **Method:**

  `POST`

* **Content-Type**

  `multipart/form-data`

* **Data Params**

   `image=[file]`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ freshness_level : 100, price : 10000 }`

## Run Test
```
python -m unittest discover tests
``` 

## License
[MIT](https://choosealicense.com/licenses/mit/)
