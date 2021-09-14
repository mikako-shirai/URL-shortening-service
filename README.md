# URL shortening service

### *UPDATE  
#### Latest files with updates including GCP and other new features are in the [GCP](https://github.com/mikako-shirai/URL-shortening-service/tree/master/GCP "GCP") folder.  
#### For more information, check the [GCP version](#GCP-version) section below.  

## Table of contents  
- [About this Project](#About-this-Project)  
    - [initial version](#initial-version)  
    - [GCP version](#GCP-version)  
- [Built with](#Built-with)  
- [Getting Started](#Getting-Started)  
    - [Prerequisites](#Prerequisites)  
    - [Installation](#Installation)  
- [Usage](#Usage)  
  
  
## About this Project  
URL shortening web service which provides short aliases and custom aliases redirecting to original URLs.  

### initial version  
Initial code only uses  
- Python  
- [Flask][Flask]  

and is a very simple web application which shortens a URL by creating a short URL alias with a 6 characters long generated key.  
Instead of using a Web database, it stores all the information (original URLs and aliases) to a JSON file and uses a text file to check existing keys to avoid duplication.  

### GCP version  
In addition to the short link feature, 1. default expiration time, 2. custom link feature, 3. custom expiration feature and 4. simple link analysis were added.  
Users can create a custom URL alias with characters of their choice and can also set a custom expiration date to both short links and custom links.  

Instead of using JSON, it uses a NoSQL document database [GCP Firestore][Firestore] to manage all the data by deploying the application to [GCP App Engine][App Engine].  

(to see an example : https://short-321807.an.r.appspot.com/)  
  

## Built with  
This project is built using the following frameworks/services  
- [Flask][Flask]  
- [GCP Firestore][Firestore]  
- [GCP App Engine][App Engine]  
- [unittest][unittest] (work in progress)  
- ~~[gRPC][gRPC]~~ (work in progress)  
  

## Getting Started  
### Prerequisites  
- [python-dateutil][python-dateutil]  
```
$ pip install python-dateutil
```  
- [Flask][Flask]  
```
$ pip install Flask
```  
- [Firestore][Firestore]  

&ensp;&ensp;&ensp;follow this [document](https://cloud.google.com/firestore/docs/quickstart-servers) for setup
```
$ pip install --upgrade google-cloud-firestore
```  
- [App Engine][App Engine]  

&ensp;&ensp;&ensp;follow this [document](https://cloud.google.com/appengine/docs/standard/python3/quickstart) for setup  
- [App Engine][App Engine] Cron Service  

&ensp;&ensp;&ensp;follow this [document](https://cloud.google.com/appengine/docs/standard/go/scheduling-jobs-with-cron-yaml) for setup  
<!-- - [pytest][pytest]  
```
$ pip install pytest
```   -->
  
### Installation  
#### initial version  
1. clone this repository  
```
$ git clone https://github.com/mikako-shirai/URL-shortening-service.git
```  
2. create and activate a virtual environment  
```
$ python3 -m venv venv
$ . venv/bin/activate
```  
&ensp;&ensp;(to deactivate)  
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
5. go to http://127.0.0.1:5000/ to view the application  

#### GCP version  
1. clone this repository  
```
$ git clone https://github.com/mikako-shirai/URL-shortening-service.git
```  
2. set up Firestore  
```
$ export GOOGLE_APPLICATION_CREDENTIALS="KEY_PATH"
```  
&ensp;&ensp;*replace KEY_PATH with the path of the JSON file that contains your service account key  

3. upload cron jobs to App Engine  
```
$ gcloud app deploy cron.yaml
```  
4. deploy the application to App Engine  
```
$ gcloud app deploy
```  
5. go to https://YOUR_PROJECT_ID.an.r.appspot.com/ to view the application  
  

## Usage  
### initial version example  
![example](https://github.com/mikako-shirai/dump/blob/main/URL-shortening-service/initial.png)  

### GCP version example
![example](https://github.com/mikako-shirai/dump/blob/main/URL-shortening-service/GCP.png)  



[Flask]: https://flask.palletsprojects.com/en/2.0.x/  
[Firestore]: https://cloud.google.com/firestore/  
[App Engine]: https://cloud.google.com/appengine/  
[python-dateutil]: https://pypi.org/project/python-dateutil/  
[unittest]: https://docs.python.org/3/library/unittest.html  
[pytest]: https://docs.pytest.org/en/6.2.x/  
[gRPC]: https://grpc.io/  

