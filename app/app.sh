#!/bin/bash
if [[ -v CERT ]]; then
    echo "Updating sslcert/cert"
    echo $CERT | base64 --decode > sslcert/cert
    sha256sum sslcert/cert
fi
if [[ -v KEY ]]; then
    echo "Updating sslcert/key"
    echo $KEY | base64 --decode > sslcert/key
    sha256sum sslcert/key
fi
npm start