This project demonstrates how to use the Spotify API to retrieve an access token and interact with Spotify’s endpoints. Currently, the code includes functionality to fetch an access token. 
-
The project is written in Python and makes use of the requests library for HTTP requests and the dotenv package for managing sensitive credentials via a .env file.
-
Note: The .env file stores your sensitive Spotify API credentials and is necessary for the code to work.
-
Features

Access Token Retrieval:
-
Authenticates with Spotify's API using your Client ID and Secret.

Retrieves an access token required for making API calls.

Artist Search:
-
Will allow users to search for artists by name.

Displays information about the artist, such as their top tracks, albums, or genres.

Setup and Prerequisites
-
Prerequisites
-
Python 3.8 or higher.

pip (Python package manager).

A Spotify Developer Account to create an app and get your Client ID and Client Secret.

Installation
-
Clone this repository:

git clone:

Navigate to the project directory:

cd spotify-api-project

Install required Python libraries:

pip install -r requirements.txt

Create a .env file in the root directory and add your Spotify credentials:

CLIENT_ID=your_spotify_client_id
CLIENT_SECRET=your_spotify_client_secret

Note: The .env file stores your sensitive Spotify API credentials and is necessary for the code to work.
