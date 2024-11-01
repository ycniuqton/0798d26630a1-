# Installation guide


```commandline
apt update && apt upgrade
```


```commandline
pip3 install pipenv
apt install pipenv
```


Vào pipenv shell
```commandline
pipenv shell
pip install -r requirements.txt

```

Cài đặt docker
```commandline
apt install docker.io
apt install docker-compose

```

Sửa lại file docker-compose.yml
- update ip cho kafka

Run docker-compose
```commandline
docker-compose up -d
```


Cài đặt nginx
```commandline
apt install nginx -y
sudo apt install certbot python3-certbot-nginx -y

sudo certbot --nginx -d example.com
sudo certbot renew --dry-run

```

Cài đặt các tham số env.yaml
- key của tài khoản tương ưng trong resellvps
- ip của kafka update virtualizor event
- ip db
.. 




<br />

> Start the APP

```bash
$ python manage.py createsuperuser # create the admin
$ python manage.py runserver       # start the project
```

At this point, the app runs at `http://127.0.0.1:8000/`.

<br />

## Codebase Structure

The project is coded using a simple and intuitive structure presented below:

```bash
< PROJECT ROOT >
   |
   |-- core/                            
   |    |-- settings.py                   # Project Configuration  
   |    |-- urls.py                       # Project Routing
   |
   |-- home/
   |    |-- views.py                      # APP Views 
   |    |-- urls.py                       # APP Routing
   |    |-- models.py                     # APP Models 
   |    |-- tests.py                      # Tests  
   |    |-- templates/                    # Theme Customisation 
   |         |-- pages                    # 
   |              |-- custom-index.py     # Custom Dashboard      
   |
   |-- requirements.txt                   # Project Dependencies
   |
   |-- env.sample                         # ENV Configuration (default values)
   |-- manage.py                          # Start the app - Django default start script
   |
   |-- ************************************************************************
```

<br />

```commandline
python manage.py makemigrations
python manage.py migrate
```