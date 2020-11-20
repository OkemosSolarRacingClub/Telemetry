# Okemos Solar Racing Club's 2019 Telemetry System

Here is the public release of our 2019 Solar Car Challenge telemetry code for others to use.

### Setup

To begin, create a Google Cloud account. When you make a new account, you get a $300 free credit, which should be more than enough to cover the costs of your server. If this isn't enough, you can also apply for a grant from Google Cloud, which they accept quickly.

First you will need to make a Firebase in Google Cloud. Create a realtime database and save your access keys.

Next, modify the code attached to make it your own, and replace all instances of API keys with your own.

You will need to start an App Engine instance in Google Cloud to run this. main.py and the templates and static folders will need to be published to your GAE after adding in your Firebase keys.

The `/rpi` webhook in main.py can be modified to receive any data you want to send from the Raspberry Pi or Arduino on your car. We have included a sample speed.py that uses a hall effects sensor to calculate speed and upload it straight to our database.

Your easiest course of action is to modify your Firebase server to receive whatever data you want to, and to modify that `/rpi` webhook for any other data you want to receive.

### Help

This code was not very well polished originally, so if you have any questions, feel free to reach out and email us.
