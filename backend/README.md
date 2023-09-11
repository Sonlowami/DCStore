# DCStore API

create `.env` file at the root of the repository/directory with the following content:
```
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=dicom
MYSQL_PASSWORD=dicompass
MYSQL_DB=dicom_db_dev
```

`cd src/` then run `cat init_db.sql | sudo mysql` to create the user & database, then run `create_tables.py` to create the tables.

`python3 -m api.v1.app` from within the `src/` folder to run the app.
