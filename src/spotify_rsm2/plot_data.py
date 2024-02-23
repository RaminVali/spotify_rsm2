import logging
from typing import Optional
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import ListedColormap
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True}) # avoiding the tick label cutoffs.


# # Sonia's correlation plot
# Bring back the config file columns from usrconfig
def correlation_plot (df, img_path, config):
    '''Analyze previously-loaded data.

    This function calculates the correlation between all numerical 
    columns listed in columns_for_corr in userconfig.yml and generates a correlation plot

    Parameters
    ----------
    DataFrame object from load_data module, containing the track information for all the tracks in the playlist

    Returns
    -------
    figure : plt.figure

    ''' 
   
    playlist_data_explore_corr = df[config['columns_for_corr']]
    assert set(config['columns_for_corr']).issubset(set(df.columns.tolist())), "Error selecting columns for correlation analysis. Make sure your columns exist in the dataset."
    ax = sns.heatmap(playlist_data_explore_corr.corr(), annot=config['annotate_heatmap'])
    ax.set_title(config['corr_plot_title'])
    figure = ax.get_figure()
    figure.savefig(img_path +'playlist_data_correlation_heatmap.pdf')
    return figure


# Melissa's plot:
def single_v_album_stripplot(df, img_path, config):
    '''Analyze previously-loaded data.

    This function uses a strip plot to analyze the contrast between single tracks, 
    albums and compilations.


    Parameters
    ----------
    df: DataFrame object from load_data module, containing the track information 
    for all the tracks in the playlist
    save_path : optional path to save the files
    config: Config file to control plotting parameters
        
    Returns
    -------
    figure : plt.figure
   
    '''
    ax = plt.figure()
    ax = sns.stripplot(data=df, x='speechiness', y='album_album_type', hue='danceability')
    figure = ax.get_figure()
    ax.set_xlabel('Speechiness')
    ax.set_title(config['strip_plot_title'])
    figure.savefig(img_path +'single_v_album_analysis.pdf')
    return figure
    


def artists_bar_plot(df, img_path, config):
    '''
    This function plots the track count of every artist in
    the chosen playlist. The tile name for saving the figure
    can be controlled byt he user config.

    Parameters
    ----------
    df: DataFrame object from load_data module, containing the track information 
    for all the tracks in the playlist
    save_path : optional path to save the files
    config: Config file to control plotting parameters        
    Returns
    -------
     figure : plt.figure
    '''
    artists = df.artists.value_counts(ascending=True)[-11:].to_frame() # plot the top 10 most represented
    fig, ax = plt.subplots()
    ax.barh(artists.index, artists['count'], color = config['bar_plot_color'], edgecolor = config['endge_color'])
    ax.set_title('Top 10 Represented Artists in the Playlist')
    ax.set_xlabel('Number of tracks by the artist in the playlist')
    plt.savefig(img_path+config['bar_plot_save_name'])
    return fig


# Ramin's 3D plot
def polularity_3d_plot(df,img_path, config):
    '''
    This function plots the popularity of the tracks in the plalist vs the speechiness
    and dancibility. It is very helpful to see the correlation between the three variables.

    Parameters
    ----------
    df: DataFrame object from load_data module, containing the track information 
    for all the tracks in the playlist
    save_path : optional path to save the files
    config: Config file to control plotting parameters
        
    Returns
    -------
     figure : plt.figure
    '''
    # normalising the variables:
    x = df['speechiness']/df['speechiness'].max()
    y = df['danceability']/df['danceability'].max()
    z = df['popularity']/df['popularity'].max()

    # axes instance
    fig = plt.figure(figsize=(6,6))
    fig.set_tight_layout(False) # we get a user warning otherwise
    ax = Axes3D(fig, auto_add_to_figure=False)
    fig.add_axes(ax)

    # get colormap from seaborn
    cmap = ListedColormap(sns.color_palette(config['3d_colormap'], 256).as_hex())

    # plot
    sc = ax.scatter(x, y, z, s=40, c=x, marker='o', cmap=cmap, alpha=1)
    ax.set_xlabel('Speechiness')
    ax.set_ylabel('Danceability')
    ax.set_zlabel('Popularity')

    # legend
    plt.legend(*sc.legend_elements(), bbox_to_anchor=(1.05, 1), loc=2)

    # save
    plt.savefig(img_path+"Populalrity_3D.pdf", bbox_inches='tight')
    return fig


def plot_data(df, save_path: Optional[str], config):
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
        img_path = save_path
    else:
        img_path = config['default_img_path']
    
    # Calling all the plotting functions
    correlation_fig = correlation_plot(df, img_path, config)
    stripplot = single_v_album_stripplot(df,img_path, config)
    bar_plot = artists_bar_plot(df, img_path, config)
    plot_3d = polularity_3d_plot(df, img_path, config)

    logging.info(f'Successfully finsihed plot_data stage, response is {type(plot_3d)}')

    return correlation_fig, stripplot, bar_plot, plot_3d


