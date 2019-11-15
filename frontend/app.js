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
