# smart_book_site

#### to set up ngrok
* download and run ngrok 
`ngrok http 8000`

* copy forwarding https url to dialogflow console-> Fulfillment -> webhook -> URL, save changes

* copy and paste in /book_site/settings.py
`ALLOWED_HOSTS = [
    'your forwarding url (e.g fd24df8a5595.ngrok.io)',
    '127.0.0.1',
    'localhost'
]`


#### to start server
`docker-compose up --build -d`

#### initialize database (first database setup)
`docker-compose exec web python manage.py migrate`

#### import book data
* download and unzip into project root folder  
https://drive.google.com/file/d/1pZooiSj1wrT0-Gxp94lzdmrdK7V8tN8k/view?usp=sharing
* requests library is installed  
`pip install requests`
* ensure server is started and run import script  
`python import_books.py`

#### to access frontend
`http://localhost:8000`
#### to access browsable api
`http://localhost:8000/api/`
#### to access admin page
`http://localhost:8000/admin/`

#### to create superuser
`docker-compose exec web python manage.py createsuperuser`

#### to access database client
`docker-compose exec db psql -U django -d django`

#### stop server
`docker-compose down`
