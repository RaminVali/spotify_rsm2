import pandas as pd
import requests
import logging


def get_playlist_uri(playlist_url: str) -> str:
    '''A function that gets a spotify plalist URL and returns the 
    playlist uri to be used later on for data gathering

    Parameters
    ----------
    playlist_url : A sopotify playlist url, 
    Example: https://open.spotify.com/playlist/4oYSWmdhUMwEu0yAFA47lZ

    Returns
    -------
    playlist_uri : The playlist URI
    Example: 4oYSWmdhUMwEu0yAFA47lZ
    '''
    playlist_uri = playlist_url.split('/')[-1].split("?")[0]
    return playlist_uri



def flatten_json(list_of_json_dicts:list) -> pd.DataFrame:
    '''
    A function that flattens a list of dict like jason objects into a 
    dataframe. 

    Parameters
    ----------
    list_of_json_dicts : a list, where each item is a dictionary like jason reponse 

    Returns
    -------
    df : A flattened dataframe where the column names are the keys of the dictionary like json
    response
    '''
    df = pd.DataFrame()
    for item in list_of_json_dicts:
        df = pd.concat([df,pd.json_normalize(item, sep='_')])
    return df



def authenticate(client_id:str, client_secret:str) -> dict:
    '''Authenticate the user to the spotify api and get a bearer token valid
    for one hour. 

    Parameters
    ----------
    client_id : str
        The client id from spotify webapp

    client_secret : str
        The client secret from spotify webapp

    Returns
    -------
    headers : dict
        Dictionary containing the acess token in the header form to be used in API calls later
    '''

    url = 'https://accounts.spotify.com/api/token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    data = {
    'grant_type':'client_credentials',
    'client_id': client_id,
    'client_secret':client_secret
    }

    try:
        auth_req = requests.post(url, headers=headers, data =data) # authentication request post

        logging.info(f"Sucessful authentication: Status Code {auth_req.status_code} on url{url}")
        access_token = auth_req.json()['access_token']
        headers = {'Authorization': f'Bearer {access_token}'}

    
    except Exception as e:
        logging.error(f'Error authenticating on {url}, exc_info = True')
        e.add_note(f'Error authenticating on {url}, exc_info = True')

    return headers



def get_track_ids(playlist_uri : str, headers : dict) -> list:
    ''' Retrieve track ids form a playlist on spotify

    This function makes an HTTPS request to the spotify API and retrieves track ids for your 
    selected plalist. The data is returned as a list.

    Parameters
    ----------
    playlist_uri : The playlist URI
    headers : header contaning the bearer token

    Returns
    -------
    track_ids : a list of all the track ids in the playlist
    '''
    playlist_endpoint = f'https://api.spotify.com/v1/playlists/{playlist_uri}/tracks'
    offset = 0
    playlist_pages = []

    # Looping as the json is cut off at 100, and playlist can have more than 100 songs
    while True:
        response = requests.get(playlist_endpoint+f'?offset={offset}', headers=headers)
        playlist_total = response.json()['total']
        playlist_pages.append(response.json()['items'])

        offset += 100
        if offset>playlist_total:
            break

    logging.info(f"There are {playlist_total} tracks in this playlist")
    logging.info(f"Number of pages in playlist_pages: {len(playlist_pages)}")

    track_id_df = flatten_json(playlist_pages)
    track_ids = track_id_df['track_id'].to_list()

    return track_ids



def get_track_data(track_ids:list, headers:dict) -> pd.DataFrame:
    '''
    This function loops through the list of track ids provided and retrives track information
    and acoustic features for each track calling two seperate API end points. The results are then
    consolidated into a dfataframe which is returned.

    Parameters
    ----------
    track_ids
    headers : header contaning the bearer token

    Returns
    -------
    track_ids : a list of all the track ids in the playlist

    '''
    start = 0
    end = len(track_ids)
    step = 50 # API only accepts a maximum 50 id values

    track_info=[]
    track_feature_info = []
    # send track ids in chucnks of 50 comma seperated strings to the API and append the 
    # response to appropriate lists.
    for i in range(start, end, step):
        x = i
        id_chunk = ','.join(track_ids[x:x+step])

        track_api_endpoint = f'https://api.spotify.com/v1/tracks?ids={id_chunk}'
        response_track = requests.get(track_api_endpoint, headers=headers)
        track_info.append(response_track.json()['tracks'])

        track_features_endpoint = f'https://api.spotify.com/v1/audio-features?ids={id_chunk}'
        response_feature = requests.get(track_features_endpoint, headers=headers)
        track_feature_info.append(response_feature.json()['audio_features'])

    df1 = flatten_json(track_info)
    df2 = flatten_json(track_feature_info)
    df = df1.merge(df2, on = 'id', how = 'left')
    logging.info(f'Successfully retrievd track information, final dataframe shape is {df.shape}')

    assert isinstance(df, pd.DataFrame)
    
    return df

def prep_data(df:pd.DataFrame)->pd.DataFrame:
    '''
    This function receives a scarped dataframe scraped form the API and does some preprocessing 
    to extract the artist name and do key mapping. This function can be expanded in real projects to 
    handle the file preprocessing.

    Parameters
    ----------
    df : input dataframe - raw


    Returns
    ----------
    df : processed dataframe
    '''
    # # fixing the artist column
    def get_artist(row):
        sep = 'type'
        result = str(row).split('name')[1:][0].split(sep,1)[0]
        result = result.replace("': '",'').replace("', '",'')
        return result
    df['artists'] = df['artists'].apply(get_artist).copy()


    # mapping keys column to actual keys
    music_dict = {0:'C',1:'C', 2:'D', 3:'D#', 4:'E', 5:'F', 6:'F#', 7:'G', 8:'G#',9:'A', 10 :'A#', 11:'B'}
    df['key'] = df['key'].apply(lambda x:music_dict[x])

    assert isinstance(df, pd.DataFrame)

    return df



def load_data(config:dict):
    ''' Retrieve data from the spotify API

    This function takes user credentials and a spotify plaift url, and returns a dataframe with 
    all the assocated track information for that url. 

    Parameters
    ----------
    config : dict the configuration file


    Returns
    -------
    DataFrame object, containing the track information for all the tracks in the playlist

    '''
    # Parsing the config file for credentials
    client_id = config['client_id']
    client_secret = config['client_secret']
    playlist_url = config ['playlist_url']

    # inner function calls to authenticate, retirve and prep data
    playlist_uri = get_playlist_uri(playlist_url)
    headers = authenticate(client_id, client_secret)
    track_ids = get_track_ids(playlist_uri, headers)
    df_raw = get_track_data(track_ids,headers)
    df = prep_data(df_raw)
    
    logging.info(f'Successfully finsihed load_data stage, final dataframe shape is {df.shape}')


    return df
