/*##############################################################################
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
##############################################################################*/
var express = require('express');
var fs = require('fs');
var http = require('http');

var app = express();
var path = require('path');

app.use(express.static('./'));

var options = {
    key: fs.readFileSync( 'sslcert/localhost.key', 'utf8' ),
    cert: fs.readFileSync('sslcert/localhost.cert', 'utf8'),
    requestCert: false,
    rejectUnauthorized: false
};

var https = require('https');

var httpServer = http.createServer(app);
var httpsServer = https.createServer(options, app);

app.get('/', function(req, res) {
    console.log(path.join(__dirname + '/index.html'));
    res.sendFile(path.join(__dirname + '/index.html'));
});

httpServer.listen(8080);
httpsServer.listen(8443);
