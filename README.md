# Django + Celery + PostgreSQL + NGINX + Docker


This project is a real-time online monitoring website which was built on Django and running on NGINX using Docker. It displays the information of all the devices derived from a LabVIEW server(There is a mock-up LabVIEW server in Sim LabVIEW server.)


There are 4 apps which are
* Account:

This app is about user log in/out. The usernames and passwords are save in the database. But, it bases on the user information on LabVIEW server. While the user type the wrong username of password, it will update the usernames and passwords.

* Favorite:

In this app, user could add devices to your favorite page so that user could quickly find the device information.
* Main:

This is the homepage. Most of the utilities are saved here.
* Search:

It includes the function of search bar, plot devices information, and search plot.
