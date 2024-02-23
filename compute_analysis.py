import pandas as pd 
import logging

#df = pd.read_csv('../data.csv')

def compute_analysis(df):
    '''
    This function analyses the selected playlist and outputs the following:

    - Total number of tracks in the playlist
    - Total number of artists reprersented in the playlist
    - Total duration of the playlist

    Parameters
    ----------
    df : Dataframe object from load data


    Returns:
    --------
    None (Print statements for the above as per the assignment requirements)
    
    '''

    try :
        num_tracks = df.shape[0]
        print(num_tracks)
        duration = round(df['duration_ms_y'].sum()/3600000)
        num_artist = len(df['artists'].unique())
        analysis_dict = {'Number of Tracks': num_tracks, 'Playlist Duration (Hours)': duration, 'Number of Artists':num_artist}
        analysis_df = pd.DataFrame(analysis_dict, index=[''])
        return analysis_df

    except  Exception as e:
        e.add_note('Did not find the dataframe to do analysis on')
        logging.error('Error loading data for analysis')

