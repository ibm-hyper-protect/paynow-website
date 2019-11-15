# Frontend Disaster Donations Application

This is the frontend application that serves the disaster donations
website. It's a fairly simple node.js (Express) app, serving static
HTML. The donations page uses AJAX to call to the backend, running on
the same or another machine, to retrieve and save donations
information.

As with the backend, you can run this app locally, or deploy it to a
VM in a cloud environment. For example, deploy it to an [IBM Cloud
Hyper Protect Virtual
Server](https://cloud.ibm.com/catalog/services/hyper-protect-virtual-server)
instance. With this option, you can ensure that the storage used for
this app is encrypted. Run the backend on the same service, and this
is covered too.


## Modify the Application Before Running

The app can largely be used as-is. Edit [`donate.js`](./donate.js) to
change the `BACKEND` variable to the hostname where the backend
application (also in this repo) is running.


## Build and Run the Application

Run the application standlone with

```
npm install
npm start
```

in this directory. The application listens both on port `8080` and
`8443`. Alternatively, build and run the application in a Docker
container:

```
docker build -t disaster-frontend .
docker run -d -p8080:8080 -p8443:8443 disaster-frontend
```


## Test the Application

Use a web browser to navigate to
[`locahost:8080`](http://localhost:8080) and confirm that the
donations homepage loads. (Or, of course, whichever host you're
running it on.)

Navigate to the donations page try out that functionality, driving
AJAX calls to issue `GET` and `POST` requests to the backend
application. You can view the console to check these network calls are
functioning correctly.

Note that your web browser may block requests if the frontend and
backend are running on different machines, due to cross-origin
resource sharing (CORS). Either disable these, or better, run a
[reverse proxy](../proxy) in front of both services.
