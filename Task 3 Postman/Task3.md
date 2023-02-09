# Table of Content

* [Task 3: Rest API with Postman](#task-3-rest-api-with-postman)
* [Step 1: Postman Configuration](#step-1-postman-configuration)
* [Step 2: Authentication](#step-2-authentication)
* [Step 3: API Cross-Site Request Forgery Prevention](#step-3-api-cross-site-request-forgery-prevention)
* [Step 4: GET SD-WAN Fabric Devices](#step-4-get-sd-wan-fabric-devices)
* [Step 5: GET SD-WAN Devices Status](#step-5-get-sd-wan-devices-status)
* [Step 6: GET SD-WAN Devices Counters](#step-6-get-sd-wan-devices-counters)
* [Step 7: GET SD-WAN Interface Statistics](#step-7-get-sd-wan-interface-statistics)
* [Step 8: Add User Group](#step-8-add-user-group)
* [Step 9: Add User](#step-9-add-user)
* [Step 10: Generate code with Postman](#step-10-generate-code-with-postman)

## Task 3: Rest API with Postman

## Step 1: Postman Configuration

A Postman environment is a list of variables that can be used to easily switch between different environments. By simply modifying the vManage username, password, port and hostname in the case of your environment, you can access and interact with different Cisco SD-WAN fabrics. The variables that are defined in the environment can be re-used also throughout the API calls that are defined in the collection.

A Postman collection is a group of API calls that define endpoints or resources that are available for that specific API. The collection also includes other parameters, headers, or authentication methods that are needed to successfully complete the call.

Login to the windows machine using RDP IP and Credentials in the Main Page and launch the Postman Application

Before running any exercise, verify that your Postman configuration has SSL certificate verification disabled

![postman](/images/pm-1.png)

```A sample Postman Collection and a set of environment variables are already created to save time```

![postman](/images/pm-2.png)

![postman](/images/pm-3.png)

## Step 2: Authentication

The first step in interacting with an API is usually authentication. Authentication ensures that only legitimate users have access to the API.

In your Cisco-SD-WAN collection, you can see that the first API call that you have is called Authentication and is in a folder named Authentication.

The Authentication call is a POST call.
To define the endpoint for the authentication call, you use the environment variable {{vmanage}}. These values will be replaced with the ones you have defined in the environment variables

The resource that you are sending the API call to is j_security_check.

After the variables are replaced, the resulting endpoint for authentication is "https://{ip_address}.com/j_security_check"

Under the Headers tab, you define the Content-Type header.

For Cisco SD-WAN authentication, the type is application/x-www-form-urlencoded.
The username and password are URL-encoded in the Body or the request and are sent as key value pairs j_username and j_password. You will populate the values for the username and password from the environment variables with the same names.

These are all the parameters that you need to authenticate to the vManage instance: the endpoint, the method, the header, and the body.

![postman](/images/pm-4.png)

The body of the returned information should be empty and the status should be 200 OK if everything went well. This status means that the user was successfully authenticated. Notice that the response returns a Cookie named JSESSIONID. You use this cookie in the subsequent API calls in the next sections of this Lab. This cookie has a limited lifetime and is a temporary representation of the successful authentication of the admin account.

![postman](/images/pm-5.png)

## Step 3: API Cross-Site Request Forgery Prevention

This feature adds protection against Cross-Site Request Forgery (CSRF) that could occur when using Cisco SD-WAN REST APIs. The system provides this protection by requiring a CSRF token with API requests. This token is need to POST requrest.

Execute the GET token request to generate the XSRF Token

![postman](/images/pm-6.png)

## Step 4: GET SD-WAN Fabric Devices

After you successfully authenticated and obtained the JSESSIONID cookie, you can now obtain the data that you want from the Cisco SD-WAN REST API.
The Fabric Devices API call uses the GET method and the /dataservice/device endpoint to obtain a JSON-formatted list of all the devices that are part of the SD-WAN fabric.
After you press Send in Postman for this first API call, you should see a response similar to the following:

![postman](/images/pm-7.png)

If you do not get a response, check to make sure that the status code response is 200 OK, if not the most probable cause is that your JSESSIONID cookie has expired and you need to re-authenticate once more. The output in the body of the response is verbose and informative, containing extensive data about each device in the fabric.

The next API in the collection is called Devices Status and uses the GET method on the /dataservice/device/monitor endpoint to obtain specific information regarding the status of all the devices in the fabric.

## Step 5: GET SD-WAN Devices Status

The next API in the collection is called Devices Status and uses the GET method on the /dataservice/device/monitor endpoint to obtain specific information regarding the status of all the devices in the fabric.
After you press Send in Postman for this first API call, you should see a response similar to the following:

![postman](/images/pm-8.png)

You can see that the JSON output is the same and consistent no matter if you get the data through the swagger documentation or Postman.

## Step 6: GET SD-WAN Devices Counters

The next API call in the Postman collection uses a GET method on the "https://{{vmanage}}:{{port}}/dataservice/device/counters" resource.

![postman](/images/pm-9.png)

## Step 7: GET SD-WAN Interface Statistics

Next, you try to obtain interface statistics for the devices that are part of the SD-WAN fabric. The endpoint that will return extensive statistics for all the interfaces on all the devices in the fabric is /dataservice/statistics/interface

![postman](/images/pm-10.png)

Depending on the size of the fabric, this call can take a large amount of time to return data or time out entirely. You can clearly see the power of the API, in which, with one call you can obtain extensive statistics for all the interfaces on all the devices in the fabric. By passing different parameters with this API call, like specific time intervals, specific devices or even specific interfaces, the output can be limited significantly.

Explore the other API GET calls in the postman collections and observe the results

## Step 8: Add User Group

Goto the admin tasks folder and explore “Add User Group” API call.
This being a POST request needs the XSRF token. The token is taken as a variable and is loaded in the environment variable from the previous GET call

![postman](/images/pm-11.png)

Look at the Request body it will create a user group called “demogrp” with read and write access to “Manage user” feature

![postman](/images/pm-12.png)

## Step 9: Add User

The next call with let us create a user “demouser” and assign it to “demogrp”.

![postman](/images/pm-13.png)

## Step 10: Generate code with Postman

You have learned how to authenticate to the Cisco SD-WAN REST API and how to interact with it to extract data by using Postman. Postman has another very useful feature: code generation.
Once you build your API call, you specify the method, the endpoint, the headers, body, authentication and parameters, and then you can generate code in several programming languages that re-create the same API call in the programming language you have chosen.
The following example uses the Add User call from the collection. On the right corner of the Postman client page, there is a Code option:

![postman](/images/pm-14.png)

If you click the Code option, you can select between several programming languages, including Python, Ruby, Go, C#, C, NodeJS, JavaScript, and PHP.
If you select Python, the Authentication will be reproduced in Python by using the requests library.

The following code is in cURL, observe the inclusion of XSRF token and JSESSION ID

![postman](/images/pm-15.png)  

The following image shows the Python code generated by Postman. Use Copy to clipboard to copy the code snippet in the Postman interface, after which you can paste the code in your favorite IDE and start to use it.

![postman](/images/pm-16.png)

At the top of the code snippet, the requests library is imported, after which variables are defined for the API resource that is being accessed (url), the username and password (payload), and the headers (headers).
The response variable contains the response of the POST request and at the end, the text method of the response object is displayed to the user.
You can do the same for all the other calls you explored in this Lab and obtain the Python code for them. You can then combine them in scripts and applications for automation and network programmability purposes

```Explore the other calls in the collection at your leisure```

* [Main Menu](/README.md/#table-of-content)
