* [Task 7: SDWAN Monitoring with webhooks](#task-7-sdwan-monitoring-with-webhooks)
    * [Step 1: Confiugre vManage](#step-1-confiugre-vmanage)
    * [Step 2: Enable Webhook Server](#step-2-enable-webhook-server)
    * [Step 3: Start Webhook Server](#step-3-start-webhook-server)

# Task 7: SDWAN Monitoring with webhooks 

The Cisco SD-WAN platform provides webhooks that allow third-party applications to receive network data, when specified events occur.
* Webhooks enable push-model mechanism to send notifications in real-time.
* To retrieve alarms in real-time from vManage using the REST APIs, you need to poll for the data frequently. By using webhooks, vManage can send HTTP POST request to the external system in real-time once an alarm is received.
* Webhooks are sometimes referred to as “Reverse APIs” and you must design an API to consume or process the data that are sent via webhook.
## Step 1: Confiugre vManage 
To enable webhook notifications for pushing alarms to external systems
* Goto Monitor > Logs Click on Alarm Notifications

 ![postman](/images/wh1.png)


* Click Add Alarm Notification
* Enter a Name – “webhook_test”
* Select Severity – Critical & Major
* Select Alarm Name – Control vBond State Change
* Check Webhook Check box
* Enter the webhook server URL, username, and password for webhook
    * If webhook server does not have authentication configured, please provide simple username and password, that are test and test, respectively.
* Webhook URL should be set to http://198.18.133.100:5001/
* Webhook Threshold – 10 
* Select All Devices option and click Add to complete the webhook settings

![postman](/images/wh2.png)

* Enable Alarm notifications in Administration settings of vManage.

![postman](/images/wh3.png)

## Step 2: Enable Webhook Server

Set up webhook server to accept notifications sent from vManage.
* To accept HTTP post requests sent from vManage, you need to enable HTTP web server and design API route.
* The “webhook.py” script shown below spins up flask web server listening on port 5001 for HTTP POST request.
* Defined webhook() function accepts the POST request at route http://198.18.133.100:5001/ and extracts the data from request and prints with Indent.
```
cat webhook.py 
```
```python
from flask import Flask, request, jsonify
import json
import os
import time
import datetime
import pytz

app = Flask(__name__)

@app.route('/',methods=['POST'])
def webhook():
    if request.method == 'POST':
       print("Data received from Webhook is: ", (json.dumps(request.json, indent=4)))
       return "Webhook received!"

app.run(host='0.0.0.0', port=5001)
```
## Step 3: Start Webhook Server
On ubuntu command prompt, run the command python webhook.py to spin up HTTP webhook server.
```
python3 webhook.py 
 * Serving Flask app 'webhook'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5001
 * Running on http://198.18.133.100:5001
Press CTRL+C to quit
```

* Trigger alarm by clearing control connections on vManage
* SSH to vManage and give the command “clear control connections”

```
python3 webhook.py 
 * Serving Flask app 'webhook-1'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5001
 * Running on http://198.18.133.100:5001
Press CTRL+C to quit
```
```json
Data received from Webhook is:  {
    "suppressed": false,
    "devices": [
        {
            "system-ip": "10.10.10.10"
        }
    ],
    "eventname": "control-vbond-state-change",
    "type": "control-vbond-state-change",
    "rulename": "control-vbond-state-change",
    "component": "Control",
    "entry_time": 1674845032974,
    "statcycletime": 1674845032885,
    "message": "vBond state changed",
    "severity": "Critical",
    "severity_number": 1,
    "uuid": "a25bf9d1-8628-465e-943f-c5761f948447",
    "values": [
        {
            "system-ip": "10.10.10.10",
            "new-state": "down",
            "host-name": "vManage"
        }
    ],
    "rule_name_display": "Control_vBond_State_Change",
    "receive_time": 1674845032912,
    "values_short_display": [
        {
            "host-name": "vManage",
            "system-ip": "10.10.10.10",
            "new-state": "down"
        }
    ],
    "system_ip": "10.10.10.10",
    "acknowledged": false,
    "active": true
}
198.18.1.10 - - [27/Jan/2023 18:44:06] "POST / HTTP/1.1" 200 -
Data received from Webhook is:  {
    "suppressed": false,
    "devices": [
        {
            "system-ip": "10.10.10.10"
        }
    ],
    "eventname": "control-vbond-state-change",
    "type": "control-vbond-state-change",
    "rulename": "control-vbond-state-change",
    "component": "Control",
    "entry_time": 1674845033633,
    "statcycletime": 1674845033432,
    "message": "vBond state changed",
    "severity": "Major",
    "severity_number": 2,
    "uuid": "0c76be0a-a9f7-45ea-90ed-12327f9e40e4",
    "values": [
        {
            "system-ip": "10.10.10.10",
            "new-state": "up",
            "host-name": "vManage"
        }
    ],
    "rule_name_display": "Control_vBond_State_Change",
    "receive_time": 1674845033436,
    "values_short_display": [
        {
            "host-name": "vManage",
            "system-ip": "10.10.10.10",
            "new-state": "up"
        }
    ],
    "system_ip": "10.10.10.10",
    "acknowledged": false,
    "cleared_events": [
        "f6e68c6b-5a58-4be5-9ba1-1319469bb3c4",
        "a25bf9d1-8628-465e-943f-c5761f948447"
    ],
    "active": false
}
198.18.1.10 - - [27/Jan/2023 18:44:06] "POST / HTTP/1.1" 200 -
```
The data received corresponds to the alarms that were received by vManage

![postman](/images/wh4.png)