#Imports the python wrapper for Genius Song Lyrics API and authorizes the object with the access token
import lyricsgenius as genius
access_token = 'L1lXyP9PHgtXsIzTM63zqlupMdMZt-LyBwDQ_J1e3CMU4iqsjOxpTSbNpp8gmxx2'
#This is to create and authorized object to make api calls
api = genius.Genius(access_token)

from flask import Flask, jsonify, request
from flask_cqlalchemy import CQLAlchemy

#Flask setup
app = Flask(__name__)
app.config['CASSANDRA_HOSTS'] = ['cassandra']
app.config['CASSANDRA_KEYSPACE'] = "genius"
app.config['CQLENG_ALLOW_SCHEMA_MANAGEMENT'] = True
db = CQLAlchemy(app)
#instance created


#Model definition for the database
class Records(db.Model):
    artists = db.columns.Text(primary_key=True,required=True)
    songs = db.columns.List(db.columns.Text,required=False)
    #lyrics = db.columns.List(db.columns.Text,required=False)
db.sync_db() #brings everything to the code from db

#Method to get a list of all artists in database
@app.route('/', methods = ['GET']) 
def get_artists():
    q=Records.all()
    count = q.count()
    artists=[]
    for i in range(count):
        artists.append(q[i]['artists'])
    return jsonify(artists)

#Method to get a list of all songs by an artist
@app.route('/<artist>', methods = ['GET'])
def get_songs(artist):
    q = Records.get(artists=artist)['songs']
    return jsonify(q)

#Search for lyrics of the song using the genius API and display it if found
@app.route('/<artist>/<song>', methods = ['GET'])
def get_lyrics(artist,song):
    
    q = Records.get(artists=artist)['songs']
    if song in q:
        data = api.search_song(song) #external API call
        lyrics = data.lyrics
    else:
        return jsonify({'error':'unable to find lyrics'}), 404
    return jsonify(lyrics)

#Serving the app over https using self signed certificates
if __name__ == '__main__':
    app.run('0.0.0.0', port=8080, ssl_context=('server.crt', 'server.key') ) #generate using openSSl

