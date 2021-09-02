# URL shortening service

### *UPDATE  
Latest files with updates including GCP and other new features are in the folder [GCP](https://github.com/mikako-shirai/URL-shortening-service/tree/master/GCP "GCP")  
For more information, please check [GCP version](#GCP version) section below.

## Table of content
- [About this Project](#About-this-Project)  
    - [initial version](#initial-version)  
    - [GCP version](#GCP-version)  
- [Built with](#Built-with)  
- [Getting Started](#Getting-Started)  
    - [Prerequisites](#Prerequisites)  
    - [Installation](#Installation)  

## About this Project  
URL shortening web service which provides short aliases and custom aliases redirecting to original URLs.  

### initial version  
Initial code only uses  
- Python  
- Flask  
and is a very simple web application which shortens a URL and create a short alias with a 6 characters long generated key.  
Instead of using a Web database, it stores all the information of original URLs and aliases to a JSON file and uses a text file to check existing keys to avoid duplication.  

### GCP version  
example : https://short-321807.an.r.appspot.com/  
![example](https://github.com/mikako-shirai/dump/blob/main/URL-shortening-service/Screen%20Shot%202021-09-03%20at%200.46.22.png)

## Built with  
This project is built using the following frameworks/services  
- Flask  
- GCP App Engine  
- GCP Firestore  
- pytest (work in progress)  
- gRPC (work in progress)  

## Getting Started  
### Prerequisites  
- Flask  
```
$ pip install Flask
```  
- pytest  
```
$ pip install pytest
```  
  
### Installation  
1. clone this repository  
```
$ git clone https://github.com/mikako-shirai/URL-shortening-service.git
```  
2. create and activate a virtual environment  
```
$ python3 -m venv venv
$ . venv/bin/activate
```  
(to deactivate)  
```
(venv)$ deactivate
```  
3. install Flask in the virtual environment  
```
(venv)$ python3 -m pip install flask
```  
4. run main.py  
```
(venv)$ pytho3 main.py
```  
5. go to http://127.0.0.1:5000/ to view the web application  
