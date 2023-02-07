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