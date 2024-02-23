from . import load_data
from . import compute_analysis
from . import plot_data
from typing import Optional
import matplotlib.pyplot as plt
import yaml
import requests
import pandas as pd
import logging
import matplotlib.pyplot as plt
import os


dirname = os.path.dirname(__file__)
logging.basicConfig (level = logging.INFO, filename=os.path.join(dirname,'../../logging.log'))


class Analysis:
    '''Main Class ofr the analysis of the spotify data.
    The load_data, compute_analysis and plot_data methods run
    on this class.
    '''
    def __init__(self, analysis_config: str) -> None:

        

        CONFIG_PATHS = [os.path.join(dirname,'../../configs/system_config.yml'), 
                        os.path.join(dirname,'../../configs/user_config.yml'),]


        # add the analysis config to the list of paths to load
        paths = CONFIG_PATHS + [analysis_config]

        # initialize empty dictionary to hold the configuration
        config = {}

        # load each config file and update the config dictionary
        for path in paths:
            with open(path, 'r') as f:
                this_config = yaml.safe_load(f)
            config.update(this_config)
        self.config = config

    def load_data(self) -> pd.DataFrame:
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
        #data = requests.get('/url/to/data').json()
        self.data = load_data.load_data(self.config)
        return self.data
        

    def compute_analysis(self) -> pd.DataFrame:
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
        output = compute_analysis.compute_analysis(self.data)
        return output


    def plot_data(self, save_path: Optional[str]=None) -> plt.Figure:
        '''
        Main plotting function, calling specialised plotting functions to 
        plot a range of values within the data.
        
        Parameters
        ----------
        df: DataFrame object from load_data module, containing the track information 
        for all the tracks in the playlist
        save_path : optional path to save the files
        config: Config file to control plotting parameters
            
        Returns
        -------
        figure : plt.figure 4 figures
        '''

        if save_path:
            os.mkdir(save_path)
        plot_data.plot_data(self.data, save_path, self.config)
        plt.show()
        plt.show()
        plt.show()
        plt.show()


    def notify_done(self, message='Your Spotify data analysis is now complete.') -> None:
        ''' Notify the user that analysis is complete.

        Send a notification to the user through the ntfy.sh webpush service.

        Important Note
        ---------------
        You must subscribe to the specified topic name in ntfy.sh! 
        See topicname in userconfig.yml for this module's topic name.

        Parameters
        ----------
        message : str
        Text of the notification to send

        Returns
        -------
        None

        '''
        
        requests.post(f"https://ntfy.sh/{self.config['topicname']}", 
            data=message.encode(encoding='utf-8'))
        

### Running in concole: - It works this way
# analysis_object = Analysis('../configs/analysis_config.yml')
# analysis_object.load_data()
# analysis_output = analysis_object.compute_analysis()
# print(analysis_output)
# analysis_object.notify_done()
# analysis_object.plot_data() # sample path: '../img2/'


