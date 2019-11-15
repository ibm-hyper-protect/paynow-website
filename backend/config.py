"""This module is to configure app to connect with database."""

import os
from pymongo import MongoClient

DEBUG = True
USERNAME = os.environ.get('USERNAME')
PASSWORD = os.environ.get('PASSWORD')

uri = 'mongodb://' + USERNAME + ':' + PASSWORD +'@' + os.environ.get('ENDPOINT') + '/?ssl=true&ssl_ca_certs=cert.pem'
DATABASE = MongoClient(uri, replicaset=os.environ.get('REPLICASET'))[os.environ.get('DBNAME')]
