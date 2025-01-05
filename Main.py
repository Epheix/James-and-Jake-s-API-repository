#Spotify Access Tokens for this to work
from dotenv import load_dotenv
import os
import base64
from requests import post, get #Allows post, get requests
import json

#this loads the Spotify ID and Secret (Jake's spotify)
load_dotenv()

client_id = os.getenv("CLIENT_ID") #Obtains client ID from the .env file
client_secret = os.getenv("CLIENT_SECRET") # Obtains client secret from the .env file
#This section gets the token to access the API
def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64= str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
    "Authorization": "Basic " + auth_base64, #Sending verification data so the access token can be retrieved
    "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"] #Token will be parsed into a field called access token
    return token

def get_auth_header(token): #Automatically constructs the headers when making additional requests
    return {"Authorization": "Bearer " + token}


#This will enable an artist to be searched and the artists ID to be returned for obtaining information about the artist
def artist_search(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1" #Gives a query to the API, is given the artist name, and will then return the most popular artist with that name
    
    query_and_url = url + query
    
    result = get(query_and_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0: #If there is no result from the json regarding artists/items, we can assume no such artist exists and will return that information to the user
        print("No artist with this name exists...")
        return None
    
    return json_result[0]
    
def get_artist_id(token):
    artist_input = str(input("Please enter an artist: "))
    result = artist_search(token, artist_input)
    print(result["name"]) #Used for testing purposes, shows the name spotify sends back based on the user input
    artist_id = result["id"]
    return artist_id

def artist_top_songs(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks" #given artist id, will search through the artists top 10 tracks
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

def main_loop():
    token = get_token()
    artist_id = get_artist_id(token)
    while True:
        num_inp = input("Please enter the desired number for the information about the selected artist. \n1.) Artists Top Songs \n")
        try:
            value = int(num_inp)
            break
        except ValueError:
            print("Please select a correct number")
    if value == 1:
        print("Here is the list of the top 10 songs by the artist:")
        song_list = artist_top_songs(token, artist_id)
        for i, song in enumerate(song_list): #We use enumerate to get both the index and value for the item, 
            print(f"{i+1}. {song['name']}")
main_loop()   

