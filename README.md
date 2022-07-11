# Django + Celery + PostgreSQL + NGINX + Docker

This project is a real-time online monitoring website which was built on Django and running on NGINX using Docker. It displays the information of all the devices derived from a server built by LabVIEW. There are some features about this website.

1. Real-time web page: updates the page with AJAX every 5 secs.
2. Responsive Web Design.
3. Database connection: customized web services can save users' most care devices.
4. ChartJS: dynamic images which show the values near the cursor.
5. Search bar
6. Proxy using NGINX.

<br>

---
## Demo video(youtube) and photo preview
There is a demo video on <a href='https://youtu.be/Dcex47DQm7w'>youtube</a>.

* log in pic
* main
* fav setting
* search bar
* plot


---
## Installation

### Environment
* Windows 10
* Docker 4.8.2
* Python 3.10.4

### Steps
1. Install Docker Desktop on its official website, and make it in running status. 
Docker Desktop official website link is <a href='https://www.docker.com/products/docker-desktop/'>here</a>.
2. Download this depo

`> git clone https://github.com/wayne87140/Docker_NGINX_Django `

3. Run in cmd or double click SimLabVIEWServer.py in SimLabVIEWServer folder

`> python SimLabVIEWServer.py`

4. Run in cmd or double click Install Web Server.bat

`> Install Web Server.bat`

5. Open web browser to visit the website(<a href='127.0.0.1:8600'>127.0.0.1:8600</a>). Due to the late establishment of celery worker and celery beat, it's better visiting the website after few secs after step 4.

    The default port is 8600. You can change the port number at .env file(WebServer/WebServer_2022/.env).

    There are default two user accounts and passwords which are {'aaaa':'aaaa', 'bbbb':'bbbb'}.I didn't write a form to create user account here.

    The plot function is limited. It's just available at 2022.07.06 and 2022.07.07, due to the limited data.

6. If you want to stop, uninstall the web services, you can run or double click the batch file.

Stop web services

`> Stop Web Server.bat`

Uninstall web services

`> Uninstall Web Server.bat`


---
## More details
There is more detail in Sim_LabVIEW_Server.md, DBdesign.md, and Celery.md.

<br>

- ### Sim_LabVIEW_Server.md

Briefly introduce server built by LabVIEW, and have a demo of server and client communication with TCP/IP.

<br>

- ### DBdesign.md

In this article, I explained how I designed the database model, and how and why I improved the original model.


<br>

- ### Celery.md
It explains the steps of setting Celery and what the tasks do.

