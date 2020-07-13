# Simple CMS API

Simple CMS API is an API that allows you to manage users and customers.

What you will find in this README:

- [1. Project requirements](#1-project-requirements)
- [2. Architecture](#2-architecture)
    - [2.1. Docker](#21-docker)
        - [2.1.1. cms_api container](#211-cms_api-container)
        - [2.1.2. postgres container](#212-postgres-container)
        - [2.1.3. localstack container](#213-aws-s3-container)
    - [2.2. Users](#22-users)
    - [2.3. Customers](#23-customers)
    - [2.4. API endpoints](#24-api-endpoints)
        - [2.4.1. Users API endpoints](#241-users-api-endpoints)
        - [2.4.2. Customers API endpoints](#242-customers-api-endpoints)
        - [2.4.3. OAuth2 authentication endpoints](#243-oauth2-authentication-endpoints)
- [3. Getting started](#3-getting-started)
    - [3.1. Clone the project](#31-Clone the project)
    - [3.2. Environment variables](#32-environment variables)
    - [3.3. Build the docker images and start the containers](#33-build-the-docker-images-and-start-the-containers)
    - [3.4. Run migrations](#34-Run migrations)
    - [3.5. Configure Localstack's AWS S3](#35-configure-Localstack's-aws-s3)
    - [3.6. Run collectstatic](#36-run-collectstatic)
    - [3.7. Create a superuser](#37-create-a-superuser)
    - [3.8. Register an application](#38-register-an-application)
    - [3.9. Use the API](#39-use-the-api)
- [4. Running tests](#4-running-tests)


# 1. Project requirements
These are the requirements that this project meets:
- [x] The API is only accessible to registered users providing an authentication mechanism
- [X] Any user can perform any CRUD operation on customers
- [X] Required fields for a customer are: id, name and surname. Photo is an optional field
- [X] Customers must have a reference to the user who created it and to the last user who updated it
- [X] Only admin users can perform CRUD operations on users
- [X] Tests implemented for the solution
- [X] Make the project set-up easy for newcomers
- [X] Follow OAuth 2 protocol for authentication
- [X] Use Docker, Vagrant or other tools to make it easier to configure development environments
- [X] Good README file with a getting started guide

# 2. Architecture
The project uses Docker to run three containers: the API, a Postgres database and a AWS S3 service (Localstack).

## 2.1. Docker

### 2.1.1. cms_api container
This container runs a Django Rest Framework powered API.

### 2.1.2. Postgres container
This container runs a Postregres database, which serves as the data store for the API.

### 2.1.3. AWS S3 container
This container runs a service which emulates AWS services. For this project we only need S3.

## 2.2. Users
**Users** interact with the API. These are the fields that a user has:
* id (required)
* username (required)
* password (required)
* is_staff (required. Defaults to False)
* email
* first_name
* last_name
* last_login
* date joined

There are 2 kind of users: 
* **normal**: if the field *is_staff*=*False*. They can only perform CRUD operations on customers.
* **admin**: if the field *is_staff*=*True*. They can perform CRUD operations on other users and on customers.


## 2.3. Customers
**Customers** can perform CRUD operations on *customers*. These are the fields that a customer has:
* id (required)
* name (required)
* surname (required)
* photo
* created_by
* updated_by

## 2.4. API endpoints
### 2.4.1 Users API endpoints
- *List* or *Create* users: *http://localhost:8000/users/*
    ````bash
    # GET example
    curl --request GET 'http://localhost:8000/users/' \
    --header 'Authorization: Bearer p5k70mKOHElwCiVURov6GjabuLVTNj'
  
    # POST example
    curl --request POST 'http://localhost:8000/users/' \
    --header 'Authorization: Bearer p5k70mKOHElwCiVURov6GjabuLVTNj' \
    --form 'username=monkey' \
    --form 'password=supersecretpassword'
    ````
    
- *Retrieve*, *Update* or *Delete* users: *http://localhost:8000/users/{user_id}*
    ````bash
    # PUT example
    curl --request PUT 'http://localhost:8000/users/6/' \
    --header 'Authorization: Bearer p5k70mKOHElwCiVURov6GjabuLVTNj' \
    --form 'username=monkey' \
    --form 'password=supersecretpassword' \
    --form 'email=monkey@jungle.com' \
    --form 'is_staff=True'
  
    # DELETE example
    curl --request DELETE 'http://localhost:8000/users/7/' \
    --header 'Authorization: Bearer p5k70mKOHElwCiVURov6GjabuLVTNj'
    ````
### 2.4.2 Customers API endpoints
- *List* or *Create* customers: *http://localhost:8000/customers/*
    ````bash
    # GET example
    curl --request GET 'http://localhost:8000/customers/' \
    --header 'Authorization: Bearer p5k70mKOHElwCiVURov6GjabuLVTNj'
  
    # POST example
    curl --request POST 'http://localhost:8000/customers/' \
    --header 'Authorization: Bearer p5k70mKOHElwCiVURov6GjabuLVTNj' \
    --form 'name=John' \
    --form 'surname=Doe' \
    --form 'photo=@/Downloads/john-profile-photo.png'
    ````
- *Retrieve*, *Update* or *Delete* customers: *http://localhost:8000/customers/{customer_id}*
    ````bash
    # PUT example
    curl --request PUT 'http://localhost:8000/customers/2/' \
    --header 'Authorization: Bearer p5k70mKOHElwCiVURov6GjabuLVTNj' \
    --form 'name=Jane' \
    --form 'surname=Doe' \
    --form 'photo=@/Downloads/jane-profile-photo.png'
  
    # DELETE example
    curl --request DELETE 'http://localhost:8000/customers/2/' \
    --header 'Authorization: Bearer p5k70mKOHElwCiVURov6GjabuLVTNj'
    ````
### 2.4.3 OAuth2 authentication endpoints
Authentication is based on the OAuth2 protocol and implemented using the [Django OAuth Toolkit](https://django-oauth-toolkit.readthedocs.io/en/latest/index.html) package, 

The following endpoints are available to authorize, obtain (and refresh), revoke and instrospect tokens:
```
http://localhost:8000/o/authorize/
http://localhost:8000/o/token/  # obtain or refresh a token
http://localhost:8000/o/revoke_token/
http://localhost:8000/o/introspect/
```

In order for a user to use the API, an application must be registered in the authentication server. See [3.7. Register an application](#3.7.-register-an-application) 

# 3. Getting started
## 3.1 Clone the project

```bash
> git clone https://github.com/jesusAlvSoto/simple-cms-api.git
```
## 3.2 Environment variables
Environment variables are not included in the repository, so we will have to create an *.env* file in the same folder as the *docker-compose.yaml* file
```bash
# move to the folder that contains the docker-compose.yaml file
> cd simple-cms-api

# create the .env file 
> touch .env
```
The environment variables in the *.env* are passed to the dockerfile.

For a development environment you can set these values in the *.env* file:
```
# Django-specific variables
DJANGO_DEBUG=True
DJANGO_SECRET_KEY=$xt6l&2f0vq(yc4#3q&1gfc7rz%2u&r&^kd9x6nxx*_)a%xv(0
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]

# Database variables
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=my_database_name
SQL_USER=my_database_user
SQL_PASSWORD=my_database_pass
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres

# boto3 and dajngo-storages variables
AWS_ACCESS_KEY_ID=123
AWS_SECRET_ACCESS_KEY=xyz
AWS_STORAGE_BUCKET_NAME=dev-bucket
AWS_S3_CUSTOM_DOMAIN_HOST=localhost:4572
AWS_S3_REGION_NAME=eu-west-2
AWS_S3_ENDPOINT_URL=http://localstack:4572
AWS_S3_SECURE_URLS=False

# localstack variables
LOCALSTACK_DEBUG=1

# CORS variables
CORS_ORIGIN_ALLOW_ALL=True
CORS_ORIGIN_WHITELIST=[]
```
## 3.3. Build the docker images and start the containers

```bash
> docker-compose up --build
```
We will see 3 containers running: *cms_api*, *db* and *localstack*.

## 3.4. Run migrations
Once the containers are running we are ready to execute the migrations:
```bash
> docker-compose exec cms_api python manage.py migrate
```

## 3.5. Configure Localstack's AWS S3
Before running the `collectstatic` command we must create the bucket in the *localstack* container. 
To create the bucket and make it public we will use *AWS CLI*. If you don't have the AWS CLI, first install it:
```bash
> pip install awscli
```

Run `aws configure` to create some credentials. Even though we are talking to our "fake" local AWS service, we still need credentials. Localstack requires that these details are present, but doesn't actually validate them, so we can enter dummy ones:
```bash
> aws configure
```
and follow the instructions in the terminal.

Now we can create a bucket named *dev-bucket* and assign an ACL so it is readable:

```bash
# create bucket
> aws --endpoint-url=http://localhost:4572 s3 mb s3://dev-bucket

# attach ACL
> aws --endpoint-url=http://localhost:4572 s3api put-bucket-acl --bucket dev-bucket --acl public-read
```
If we visit <http://localhost:8080/> we will see Localstack's web UI. Here we would see the list of all AWS services. We are just using S3, so we will see only the S3 service and our newly created bucket name.

And <http://localhost:4572> will show the S3 point with some additional information.

## 3.6. Run collectstatic
Now we have set up the bucket, we are ready to run the ```collectstatic``` command:

```bash
> docker-compose exec cms_api python manage.py collectstatic --noinput
```
We can now see all the uploaded files if we run:
````bash
> aws --endpoint-url=http://127.0.0.1:4572 s3api list-objects --bucket dev-bucket
````

## 3.7. Create a superuser

````bash
> docker-compose exec cms_api python manage.py createsuperuser
````
Now log into the admin panel `http://localhost:8000/admin/` with this user.


## 3.8. Register an application

Before users can authenticate against the authentication server, we need to register an application. 

To register an application make sure you are logged in. We can either go to ```http://localhost:8000/o/applications/``` (or from the admin panel ````http://localhost:8000/admin/oauth2_provider/````) and create a new application:
```bash
Name: <choose a name>
Client Type: <confidential / public>
Authorization Grant Type: < Authorization code / implicit / Resource owner password-based / Client credentials>
```
We can choose any of the grant types available in the OAuth2 protocol. Depending on which grant type you choose, you will have to follow a different workflow to obtain an access token.

Please refer to the [Django OAuth Toolkit](https://django-oauth-toolkit.readthedocs.io/en/latest/index.html) documentation for in depth details.

## 3.9. Use the API

We have finished setting up the project and we can start using the API. 

All the available the available endpoints can be found here: [2.4. API endpoints](#2.4.-api-endpoints)

# 4. Running tests

To run all the tests:
````bash
> docker-compose exec cms_api python manage.py test
````
