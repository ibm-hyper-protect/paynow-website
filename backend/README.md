# Backend Disaster Donations Application

This directory contains the backend application to the disaster
donations website.

It's a simple python application that takes in transaction data over
an exposed RESTful API (JSON payload expected), and translates into
calls to a backend Mongo DB instance.

For a cloud-based Mongo instance to use, try an [IBM Cloud Hyper
Protect DBaaS
Mongo](https://cloud.ibm.com/catalog/services/hyper-protect-dbaas-for-mongodb)
instance.


## Modify the Application Before Running

[`config.py`](./config.py) contains the hostname or IP address, and
port, of a listening Mongo DB instance. This line needs to be modified
to point to your own instance. We've used a certificate file too; in
the IBM Cloud interface above (if you're using this), download
`cert.pem` and place it in this directory.


## Build and Run the Application

Run the application standalone, with:

```
pip install -r requirements.txt
python3 run-app.py
```

The application will listen on port `5000`. Or, build and run a Docker
container:

```
docker build -t disaster-backend .
docker run -dp 5000:5000 -e PASSWORD='your_password' \
                         -e USERNAME='your_username' \
                         -e DBNAME='your_db_name' \
                         -e ENDPOINT='primary_hostname:port' \
                         -e REPLICASET='replica_set_name' disaster-backend
```

Where the application reads your Mongo instance username and password
from environment variables, passed through into the Docker container
with the `-e` flag. The base Docker image is multi-arch compatible.


## Test the Application

To confirm that the application is running, issue

```
curl 'localhost:5000/'
```

and the following JSON should be returned:

```
{
  "apiVersion": "v1.0", 
  "message": "Welcome to the Disaster Funding API", 
  "status": "200"
}
```

The application accepts a JSON payload in the form in
[`transaction.json`](./transaction.json).

```
curl -vX POST 'localhost:5000/api/v1/transactions' -d @transaction.json --header "Content-Type: application/json"
```

You can confirm this has worked using a Mongo client and checking that
the DB has been populated. For example, use [Robo
3T](https://robomongo.org). The name for the database in this pattern
is `restfulapi`, so look for objects created here.
