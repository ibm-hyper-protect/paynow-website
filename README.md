# Pay Now Website

The Pay Now Website is a simple application, that presents an interface to make payments.
The application shows how sensitive payment related information like e.g. credit card data is used.
It is recommended to run this application in a confidential computing environment where PII data in use is protected from malicious actors.

The website is a node.js Express app, serving
the site itself. The payment page has AJAX calls into the
application. The application processes these
RESTful JSON requests and stores the transaction data in memory.

The application can both be run locally, or in
the IBM Cloud, for example in a [IBM Cloud Hyper Protect
Virtual Server for VPC](https://www.ibm.com/cloud/hyper-protect-virtual-servers).

## Build and Run the Application

To build and run an application container image, 
run these commands:

```
docker build -t paynow .
docker run -it -p 8443:8443 paynow
```

## Test the Application

Use a web browser to navigate to
[`locahost:8443`](https://localhost:8443) and confirm that the
donations homepage loads. (Or, of course, whichever host you're
running it on.)

Navigate to the donations page try out that functionality, driving
AJAX calls to issue `GET` and `POST` requests.
You can view the console to check these network calls are
functioning correctly.

Note that your web browser may display a warning about a insecure connection and a invalid certificate,
as the application uses a simple self signed certificate for `CN=localhost`.
The certificate is contained in folder `sslcert`.

## Run the Application in Hyper Protect Virtual Server for VPC and validate the attestation record

You can run the application in [Hyper Protect Virtual Server for VPC](https://cloud.ibm.com/docs/vpc?topic=vpc-about-se). To do so, follow this [tutorial ](https://cloud.ibm.com/docs/vpc?topic=vpc-financial-transaction-confidential-computing-on-hyper-protect-virtual-server-for-vpc).

You can then download a zip file containing the [attestation record](https://cloud.ibm.com/docs/vpc?topic=vpc-about-attestation) and the signature file from API URL [`https://ip:8443/api/v1/attestation`](https://ip:8443/api/v1/attestation). This zip file contains the attestation record `se-checksums.txt` or `se-checksums.txt.enc` (the latter if you are using an encrypted attestation record) and the signature file `se-signature.bin`.

To verify the signature, follow these [instructions](https://cloud.ibm.com/docs/vpc?topic=vpc-about-attestation).

To validate the attestation record, compute the checksum of your contract
```
sha256sum contract.yml
```
and compare this checksum to the value for `cidata/user-data` in file `se-checksums.txt`.

