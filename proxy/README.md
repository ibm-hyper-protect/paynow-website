# Disaster Donations Nginx Proxy

IBM Cloud has support to run application as part of its Cloud Foundry
implementation. This is especially useful if you want to run an nginx
reverse proxy, with the following benefits:

- TLS certificate and domain name are created for you (allowing for an
  HTTPS-enabled website)
- Issues with CORS detecting AJAX calls to another machine disappear:
  route all calls to the proxy such that both frontend and backend
  appear to come from the same backend


## Config

In [`manifest.yaml`](./manifest.yaml), note the line

```
- name: hyper-protect-donate
```

This is the domain name to be created: this may already exist so
you'll have to choose something that isn't currently in use. You'll
end up with the hostname `hyper-protect-donate.mybluemix.net`, in this
case. (On the IBM Cloud website, looking at the details of this
deployed Cloud Foundry service, you can choose from a few other
domains, if desired.) Modify that name to something unique for you to
use.

Next, note the lines in [`nginx.conf`](./nginx.conf):

```
location /api {
  proxy_pass https://127.0.0.1:5000;
}

location / {
  proxy_pass https://127.0.0.1:8080;
}
```

Any request that comes into the proxy with `/api` in the request
(i.e., the AJAX calls from the frontend application to the backend
application), will be routed to, here, `localhost:5000`. Otherwise,
requests will be routed to `localhost:8080`. This means that requests
can come into this nginx proxy, either directly to load the website
(from the frontend application), or to send requests to the backend
application and onto MongoDB, and appear to be from the same machine,
while also being over HTTPS.

Change the IP address to the public IP(s) of the machine that's
running the frontend and backend applications.


## Deployment

Ensure you're logged into IBM Cloud:

```
ibmcloud login
```

Push this CF app:

```
ibmcloud cf push
```

It may tell you `No CF API endpoint set`. If that's the case, follow
along by first running

```
ibmcloud target --cf
```

That'll build the proxy, and start it running for you. Easy!
