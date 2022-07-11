# Database Design

A picture is worth a thousand words!

There would be a comparison between my original and redesigned one. 

The picture below is the original database model. It's also the model that used in the framework now.
>1st picture</br>1st picture</br>1st picture</br>1st picture</br>1st picture

When I was programming, the main purpose of using database was storing data, period.

I have 4 tables. They are all used to store data. 
Include:

- User : retrive users' username, password, and authentication from LabVIEW server and store here. 
- FavoriteDevice : One many-to-many relationship is between User and FavoriteDevice. 
- TaskResult : Running Celery to retrive devices' data from LabVIEW server and store here.
- T_H_Image : Save created images.

From above explaination, that means I didn't get the core value of RDB.

Here are some notes when I had "Scientific Computing with Python" class at freeCodeCamp.

> 1.  The power of the relational database lies in its ability to **efficiently retrieve data from those tables** and in particular where there are multiple tables and the relationships between those tables involved in the query.<br><br>
> 2. The basic rule to build a data model is **don’t put the same string data in twice - use a relationship instead.**

Due to the notes above, I reviewed the design again, and had some viewpoints.

1. I didn't make use of "relational" database. Few relations are created. 
2. IPs are appear too much times in DB. AvailableList, DisableList, device_IP, devices_with_tableHTML, connectinIP, and IPPort are all related to IP. 
3. Each IP maight have many images. There shall be a relation between images and IPs.

As a result, I redesigned the database model. However, I didn't apply it in this project now.

>2nd picture</br>2nd picture</br>2nd picture</br>2nd picture</br>2nd picture

In this new model, There are more relations and no string repeat twice. 
I created a bigger table, Device, that with 3 many-to-many relations with User. In real design, they are 3 different tables with foreign keys only. In addition, Device table and Image table have a one-to-many relation.By increasing relations, the efficiency would be enhanced. More codes are on Database operation instead of python. 