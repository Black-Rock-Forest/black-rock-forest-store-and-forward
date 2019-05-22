# Before Start
make sure you have installed in the RPI:
-  docker
- docker-compose 
- git

make sure you have installed in other machine:
- postman

# What's in the box?

- postgres  as database
- flask app as rest api
- mosquitto for M2M pub/sub broker 

# Step to build the project from scratch
the build proccess with docker-compose take care of everything you need to have up and runing the project in the RPI, also the containers are setup to auto restart in case the RPI is shutdown or restarted.

    ~$ git clone https://gitlab.com/german.martinez/black-forest.git
    it will ask you to login with your gitlab credentials
    ~$ cd black-forest 
    ~$ docker-compose build 
    ~$ docker-compose up 

In case you have any permission problems with  docker-compose, please run all docker-compose commands with sudo.

# Step to update the project
To avoid any merge conflics, **DO NOT CHANGE ANY IN THE black-forest project**, unless you know how to merge. 

    ~$ cd black-forest
    ~$ git pull 
    it will ask for gitlab credentials
    ~$ docker-compose stop
    ~$ docker-compose build 
    ~$ docker-compose up 

# Test
In order to know if the rest api is up and running,first make sure the the pc where you installed postman and the RPI are in the same lan:

  1) get the RPI IP address
  2) in postman create a post request
     1) in the url textbox:  http://**RPI-IP**:2323/login
     2) click in the Authorization tab and choose Basic Auth type
     3) the username is german and the password is martinez
     4) click the send button next to url textbox
     5) you should receive a json response:
         {"message": "success"}

# Store Records

Follow this steps to store a new record in the database using **GET HTTP REQUEST**.  
The format of the URL is as follow:  

Generic:

http://**RPI-IP**:2323/sensor/collector/<app_key>/<net_key>/<device_id>/?chN=n

Example:

http://10.0.0.115:2323/sensor/collector/1234/abc/x1v3/?ch1=1&ch2=2

  1) open postman
  2) use http://**RPI-IP**:2323/<app_key>/<net_key>/<device_id>/?chN=n
  3) click the send button next to url textbox
  4) after send the request if everything goes ok, you will receive a success message

# Get all records

Follow this steps to get all records in the database using a **GET HTTP REQUEST**.  

Generic:
    http://**RPI-IP**:2323/sensor/all

Example:  
    http://10.0.0.115:2323/sensor/all


  1) open postman
  2) use http://**RPI-IP**:2323/sensor/all
  3) click the send button next to url textbox
  4) in case you have records in the db you will receive a list of json   
  ```json
    [
        {
            "app_key": "1",
            "channels": {
                "ch1": "1",
                "ch2": "2"
            },
            "device_id": "3",
            "net_key": "2"
        },
        {
            "app_key": "dd",
            "channels": {
                "ch1": "1",
                "ch2": "2"
            },
            "device_id": "ff",
            "net_key": "ff"
        }
    ]
```  
    
 

 


