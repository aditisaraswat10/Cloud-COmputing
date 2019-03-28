# Genius/Lyrics App

This app is a lyrics app which retrieves the lyrics information of songs from any specific artist from external APIs.
The app also has an internal API where you have the ability to view, add and delete existing song entries that in the app. Information is returned in a JSON format.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.



The requirements file contains all the modules needed for the app.

### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be

Open command line and navigate to the directory of the folder where the app is stored.

Create a virtual environment with your preferred name with the following command.

```
python3 -m venv name_of_project
source name_of_project/bin/activate
```
The virtual environment needs to be activated with this command:
```
source name_of_project/bin/activate
```

From the app directory, run the following command:

```
python -m pip install -U -r requirements.txt
```
This command recursively installs/updates the modules in the requirement.txt in the local environment.

**Ensure these two lines are removed:**
```
cluster = Cluster(['cassandra'])
session = cluster.connect()
```

You should now be able run the app:

```
python app.py
```

This is successful if the terminal is displaying the following:

```
* Running on http://0.0.0.0:8080/ (Press CTRL+C to quit)
* Restarting with stat
* Debugger is active!
* Debugger PIN: 442-044-743
```
Clicking on the link should take you to the website.

Wrappers used:
lyricsgenius-python wrapper for genius api
flask-cqlalchemy- Python wrapper for Cassandra 

## Deployment

You will need the following before continuing:

* Docker
* Kubernetes

Setting configurations and creating clusters
```
export PROJECT_ID="$(gcloud config get-value project -q)"
gcloud config set compute/zone europe-west2-b
gcloud container clusters create cassandra --num-nodes=3 --machine-type "n1-standard-2"
```
Creating Replication Controllers for cassandra
```
wget -O cassandra-peer-service.yml http://tinyurl.com/yyxnephy
wget -O cassandra-service.yml http://tinyurl.com/y65czz8e
wget -O cassandra-replication-controller.yml http://tinyurl.com/y2crfsl8

kubectl create -f cassandra-peer-service.yml
kubectl create -f cassandra-service.yml
kubectl create -f cassandra-replication-controller.yml

kubectl scale rc cassandra --replicas=3
```
Creating keyspace and importing data from csv file
```
CREATE KEYSPACE genius WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor' : 2};
CREATE TABLE genius.records (artists text PRIMARY KEY, songs list<text>);
COPY genius.records(artists,songs) FROM '/home/songdata.csv' WITH DELIMITER=',' AND HEADER=TRUE;
```

This section will detail how to get this app ready for a cloud environment. For example, Google Cloud
Once the directory is uploaded, run the docker build command in the directory of the app:

```
docker build --tag=genius-image:1.0 .
```
Once built, it is required to tag with the link for pushing:
```
docker tag genius-image:1.0 gcr.io/genius-cloud-project/genius-image:1.0
```
Once built, It will need to be pushed:
```
docker push gcr.io/genius-cloud-project/genius-image:1.0
```
After being pushed, creating Kubernetes deployment from docker image and exposing port:
```
kubectl run genius-webapp --image=gcr.io/genius-cloud-project/genius-image:1.0 --port 8080

kubectl expose deployment genius-webapp --type=LoadBalancer --port 80 --target-port 8080
```
Check services for the IP address

## Built With

* [Cassandra](http://cassandra.apache.org/doc/latest/) - Database used
* [Flask](http://flask.pocoo.org/docs/1.0/) - Web framework used
*


## Authors

* **Aditi Saraswat** - *Initial work* - [Aditi](https://github.com/aditisaraswat10)


## Acknowledgments

* Thanks for the teaching and support through-out Arman and Felix!
