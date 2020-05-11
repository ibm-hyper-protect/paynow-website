"""This module is to configure app to connect with database."""
##############################################################################
# Copyright 2019 IBM Corp. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
##############################################################################

import os
from pymongo import MongoClient

DEBUG = True
USERNAME = os.environ.get('USERNAME')
PASSWORD = os.environ.get('PASSWORD')

uri = 'mongodb://' + USERNAME + ':' + PASSWORD +'@' + os.environ.get('ENDPOINT') + '/?ssl=true&ssl_ca_certs=cert.pem'
DATABASE = MongoClient(uri, replicaset=os.environ.get('REPLICASET'))[os.environ.get('DBNAME')]
