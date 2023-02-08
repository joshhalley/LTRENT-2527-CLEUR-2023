# Table of Content

* [Task 1: Rest API with CURL](#task-1-rest-api-with-curl)
* [Step 1: Log In](#step-1-log-in)
* [Step 2: Get a list of Devices](#step-2-get-a-list-of-devices)

## Task 1: Rest API with CURL

cURL: Linux command line application.

"https://curl.se/"

Curl has an extensive command line syntax, and being an open source project, is heavily used by developers within the field.

To begin with this task, we are going to follow a number of steps to familairize you with cURL and its operations.

In the first step, we are simply going to login to a vManage server via a API POST call, and retrieve the JSESSIONID cookie, this cookie will be used within subsequent steps.

## Step 1: Log In

•Before using various REST APIs, you must first log in to vManage.
•Specifically, execute as follows.
•A successful login saves the JSESSIONID in a cookie.

```code
curl --insecure \
     --location \
     --request POST "https://198.18.1.10/j_security_check" \
     --header "Content-Type: application/x-www-form-urlencoded" \
     --data "j_username=admin&j_password=C1sco12345" \
     --cookie-jar cookie.txt
```

From the above execution a few observations should be made from the CLI syntax.

--insecure

 This switch needs to be used in scenarios where the certificate may not be trusted.

Such scenarios where this happens, is when a certificate is present on the device which is not from a public CA, or if a private CA is in use, and the server executing the request, does not consider the certificate as trusted.

--location

Permits the operator to use a URL to interface with the server.

--request

Indicates the type of request which will be sent from CURL, in the scenario below, we are looking at a GET request.

--header

Allows the operator to provide the requisite headers that may be needed for interfacing directly with the server.

--data

The payload which is intended to be sent to the server as part of the request.

--cookie-jar

Location to save cookies which are returned during server communications.

## Step 2: Get a list of Devices

As an example of REST API, let's try "Get device list"

```code
curl --insecure \
     --location \
     --request GET "https://198.18.1.10/dataservice/device" \
     --cookie cookie.txt
```

Responses are returned in JSON format. To improve readability for humans, format it by piping it to python -m json.tool

```code
curl --insecure \
     --location \
     --request GET "https://198.18.1.10/dataservice/device" \
     --cookie cookie.txt \
     | python -m json.tool
```
