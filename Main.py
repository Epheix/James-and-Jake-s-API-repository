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
    while True:
        url = "https://api.spotify.com/v1/search"
        headers = get_auth_header(token)
        #The following gives a query to the API, is given the artist name, and will then return the most popular artist with that name
        query = f"?q={artist_name}&type=artist&limit=1" 
        result = get(url + query, headers=headers)
        json_result = json.loads(result.content)["artists"]["items"]
        #If there is no result from the json regarding artists/items, we can assume no such artist exists and will return that information to the user
        #So far however we have not found an input that will lead to no artist being found - random letters and numbers result in "Peppa Pig"
        if len(json_result) == 0: 
            print("No artist with this name exists...")
            artist_name = input("Please enter a different artist name: ").strip()
            continue
        else:
            return json_result[0]

#This will enable to get an artists spotify ID from the users input for further use    
def get_artist_id(token):
    while True:
        artist_input = input("Please enter an artist: ")
        result = artist_search(token, artist_input)
        print(f"You have selected the artist: {result['name']}")
        confirmation = input("Is this the correct artist (yes/no): ").strip().lower() #removes any whitespace and ensures no uppercase
        if confirmation in ["yes", "y",]: #List of values meaning yes, if input equal to one of the values, follows that statement
            artist_id = result["id"]
            return artist_id
        elif confirmation in ["no", "n"]:
            print("Lets try again and search for the correct artist")
        else:
            print("Invalid input, please respond with 'yes' or 'no'") #if input does not match any value given then repeats the block


#This will take in the desired artists ID and will search through their top tracks and return a json report for further use
def artist_top_songs(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks" #given artist id, will search through the artists top 10 tracks
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

#This will take in the desired artists ID and will search through just the artists albums and return the result
def artist_albums(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums?include_groups=album"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["items"]
    return json_result

#This is the main loop that will take place, it will first get the required authentication token and then ask for a user to input their desired artist
#Based on what the user desires to look at, their will either be a list of the artists top 10 tracks or a list of the artists albums
def main_loop():
    token = get_token()
    artist_id = get_artist_id(token)
    while True:
        num_inp = input("Please enter the desired number for the information about the selected artist. \n1.) Artists Top Songs \n2.) Artists Albums\n")
        if num_inp == "1" or num_inp == "2":
            break
        else:
            print("Please choose a correct nunber")
    if num_inp == "1":
        print("Here is the list of the top 10 songs by the artist:")
        song_list = artist_top_songs(token, artist_id)
        for i, song in enumerate(song_list, start=1): #We use enumerate to get both the index and value for the item, 
            print(f"{i}. {song['name']}")
    elif num_inp == "2":
        print("Here is the list of all the albums by the artist, sorted by release date:")
        album_list = artist_albums(token, artist_id)
        for i, album in enumerate(album_list, start=1): #We use enumerate to get both the index and value for the item, 
            print(f"{album['name']} | {album['total_tracks']} total tracks | ({album['release_date']})")
    else:
        print

main_loop()   

