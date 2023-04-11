### Description

**YAMDB** project is a popular artworks review platform that contains brief information about various pieces of art and gives users possibility to leave personal reviews and comments.
**YAMDB** provides API that allows to develop your own user interface to the platform and integrate it into your eco-system.

API contains methods for management of the following entities:
- Artworks (categories, genres, brief information)
- Reviews of artworks
- Comments to reviews

Also **YAMDB** provides user management service including registration, profile management and access control via API.

### Installation and launch:

**YAMDB** platofrm is build with the use of the Django framework.

In order to deploy this project you need to have installed Docker application. Below are the steps required for initial deployment of the project. Please note that exact commands may differ depends on the host operating system.

1. Clone git repository and navigate to the cloned repository in the CLI:

```
git@github.com:ead3471/api_yamdb.git
```

```
cd infra_sp2/api_yamdb
```

2. Edit .env_sample file and save as .env

3. Build images and run docker containers:

```
docker-compose up -d --build
```

4. Run migrations:

```
docker-compose exec web python manage.py migrate
```

5. Create Django superuser:

```
docker-compose exec web python manage.py createsuperuser
```

6. Collect static

```
docker-compose exec web python manage.py collectstatic --no-input
```


### API specification

Complete API specification is available at http://127.0.0.1/redoc after project deployment.

### Authors:
 - Gubarik Vladimir
 - Bogdanova Evgenia
 - Kovchegin Andrew


### Used technologies:
![Alt-Текст](https://img.shields.io/badge/python-3.7-blue)
![Alt-Текст](https://img.shields.io/badge/django-2.2.16-blue)
![Alt-Текст](https://img.shields.io/badge/djangorestframework-3.12.4-blue)
![Alt-Текст](https://img.shields.io/badge/docker-20.10.23-blue)
![Alt-Текст](https://img.shields.io/badge/nginx-1.21.3-blue)
![Alt-Текст](https://img.shields.io/badge/gunicorn-20.0.4-blue)