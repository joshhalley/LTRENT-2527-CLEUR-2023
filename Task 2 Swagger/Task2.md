# Table of Content

* [Task 2 REST API with Swagger](#task-2-rest-api-with-swagger)
* [Step 1 Open API docs](#step-1-open-api-docs)
* [Step 2 Get a List of Devices](#step-2-get-a-list-of-devices)
* [Step 3 Real Time Monitoring](#step-3-real-time-monitoring)
* [Step 4 Creat User Group](#step-4-create-user-group)

## Task 2: REST API with Swagger

Swagger-based documentation is provided through your vManage instance at

"https://vmanage-ip/apidocs"

This documentation gives you the option of interacting with the API and to see how the schema of the API is organized, and can be very helpful in building up the right syntax to use within future scripts and automation.

## Step 1: Open API docs

* Login to the following URL to access the API Docs
* "https://198.18.1.10/apidocs"
* username “admin”* password “C1sco12345”
* Observe the different categories of API calls

## Step 2: Get a list of Devices

Scroll down to Monitoring – Device Details

![swagger](/images/sw1.png)

Expand GET /device

![postman](/images/sw2.png)

Click Try it Out to Execute the API call; upon execution, scroll down and observe the CURL request and results retunred.

![postman](/images/sw3.png)

## Step 3: Real Time Monitoring

Scroll down to Real Time Monitoring – Device Contol > expand and go to GET
 /device/control/summary
![postman](/images/sw4.png)

Click Try it out, this time taking a device id from the previous output and entering it into the dialog box, follow this by clicking the button. We are using 10.3.0.1 in this example

![postman](/images/sw5.png)

Again bbserve the CURL request and results

## Step 4: Create User Group

Scroll Up to Administration – User and Group, Expand and Go to POST /admin/usergroup

![postman](/images/sw6.png)

Click Try it out > In the request body modify the name to “ciscoliveams” changing the feature from read & write to false as needed as to steer your role based access control capabilities (RBAC) and click to execute.

![postman](/images/sw7.png)

Login to vManage GUI and verify the user group
Administration > Manage users > User Groups

![postman](/images/sw8.png)

```Take some time and explore more GET calls and observe the request body and results```

* [Main Menu](/README.md/#table-of-content)