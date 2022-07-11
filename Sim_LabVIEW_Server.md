# LabVIEW Server

The real server written by LabVIEW is a powerful server for data collection in real time. Here, I just mention two functions that related to the webserver.

- ## Data collection

The server collects all the data from machines include temperature, humidity, error code, etc. Those data will be update every few seconds. To receive the data from LabVIEW server, we communicate via TCP/IP with JSON format.

- ## User creation 

Users are created here. About the user information, it includes username, passwords, and authentication about reading machines' data. 
On the other hand, our customer doesn't want to have two usernames and passwords in LabVIEW system and web server. As a result, the web server retrieves user information from LabVIEW as well.

In this simulated LabVIEW server, I just simply created a server which sends fiexed users' and machines' information.

## Demo

I wrote a server and client here. Module socket are used to communicate via TCP/IP between server and client.

Run server at cmd

`> python SimLabVIEWServer.py`

Run client at cmd

`> python SimClient.py`