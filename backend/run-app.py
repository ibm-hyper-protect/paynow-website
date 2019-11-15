# -*- coding: utf-8 -*-

from app import app

if __name__ == '__main__':
    # Running app in debug mode
    app.run(host='0.0.0.0',debug=True)
    # app.run(host='0.0.0.0',debug=True, ssl_context=('domain_cert.pem', 'key.pem'))
