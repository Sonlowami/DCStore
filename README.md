# DCStore - A Cloud-based Storage service for medical images

## About this project

DCStore is a cloud-based service for storing medical images. We provide simple and easy to use API
to interact with DICOM data. In addition, we have a user friendly web-based application that you can use to manage files if you do not want to interact with the API directly.

## Using the APIs

This section will discuss how you can use the APIs. In case you want to interact via the browser, check the browser access section.

### Installation

Currently, you can access the API through our website by prepending to the path by `/api/v1`. But, if you want, you can also host it yourself. We recommend the later as we might be short of resources to keep it online. Let's say how you actually run it locally. If you want to use the version we hosted, jump straight to the endpoints section.

#### Requirements

You will need the following basic resources:
- Python-3.6 or higher
- MySQL-5.7 or higher
- Mongo-5.0 or higher
- Redis- Latest

#### Cloning the Repo

I assume you are using SSH connection with your github. If so, you can clone the [respository](https://github.com/Sonlowami/DCStore.git) by the following command:

```
git clone git@github.com:Sonlowami/DCStore.git
```

#### Installling dependencies

Then, open the terminal on your computer and move into the root directory of the project. Once there, create a python environment. On Unix-based OS, use the following commands:

```
cd DCStore/
python3 -m venv dcenv
```
You can replace `dcvenv` by whatever you want to name your python environment. Once the environment is created, you need to activate it and install dependencies. If you use Unix, use the following commands:
```
source dcenv/bin/activate
pip install -r requirements.txt
```
#### Setting up the environment
To use run the app, there are a few environemt variables you need to set. The table below details them.

| Variable | Description |
| -------- | ----------- |
|MONGO_HOST | Mongodb host, defaults to `localhost`|
|MONGO_PORT | Mongodb port, defaults to `27017`
|MONGO_DBNAME| Name of the mongo database, defaults to `dcstore`. Make sure it is there.|
|MONGO_URI | If you are using a cloud mongodb storage tool like Mongo Atlas, you can specify the mongo uri directly with this variable. If not set, the uri name will be computed from the variables above.|
|MYSQL_HOST| MySQL host, defaults to `localhost`|
|MYSQL_PORT| Port that MySQL process is listening to, defaults to  `3306`|
|MYSQL_DB| MySQL database to connect to. No default set|
|MYSQL_USER| MySQL user to connect to. No default set|
|MYSQL_PASSWORD| MySQL password to connect to. No defaults set|
|MAIL_SERVER| The mail server to use sending verification emails to the user|
|MAIL_PORT| Port that the mail service listens to, defaults to `465`
|MAIL_USERNAME| Username to connect to|
|MAIL_PASSWORD| Password for the username|
|MAIL_USE_TLS| Defaults to `true`, and allows connection via TLS
|MAIL_USE_SSL| Defaults to `false` and allows connection via SSL3 when set to `true`|
|REDIS_HOST| Hostname or IP Address of the computer hosting a REDIS instance you want to use, defaults to `localhost`|
|REDIS_PORT| Port the redis process is listening to, defaults to `6379`|
|REDIS_DB| The redis database to connect to, defaults to `0`|
|

### Running the API service

To run the API service locally, run the following commands:
```
cd backend/src/api/v1
flask run
```
For production, you can either create a `Gunicorn` server. We refer you to [this tutorial](https://developers.redhat.com/articles/2023/08/17/how-deploy-flask-application-python-gunicorn) if you need to learn how.

You  can also use build a docker container. A docker file will be provided in subsequent updates.


### Endpoints

Regardless of whether you are querying the APIs locally, or are querying them from us, this section concerns you. Endpoints we provided are grouped into 3 main groups:
- User authentication endpoints
- Metadata querying endpoints
- File Access endpoints

If you want to test the endpoints, see the requirements and how they work, check their Swagger documentation by querying `/api/v1/apidocs` in your browser.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Authors

- [Saad Outchakoucht](https://github.com/saad-out)
- [Uwimana Lowami](https://github.com/Sonlowami)
