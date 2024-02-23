# Spotify_rsm
Team repo for DSI BRS Assignment
## Table of Contents
* [General Info] (#general-info)
* [Technologies] (#technologies)
* [Setup] (#setup)
* [Inspiration] 

## General Info
This project is a simple function to generate different sorts of graphs to analyze Spotify Playlists based on any variable you'd like. We suggest to explore danceability, speechiness and valence.

#Technologies
Project is created with:
* Python version : 3.11.5
* Bash Command
* ntfy.sh
* Among others

## Setup 
To access a Spotify API yourself, you'll need to create an account to obtain a client_id and client_secret.
Make a file called `analysis_config.yml` and have `client_id`, `client_secret` and `playlist_url` with a playlist of your choosing.
Initially the project was supposed to run on google colab, but shipping the config files to colab proved to be problematic (even when the config files are shipped in the package, google colab does not find them post import). So the `system_config.yml` and the `user_config.yml` files require to be present in the directory. 
You can take them form the repository. 
The package can be installed by running `pip install git+https://github.com/RaminVali/spotify_rsm.git`.
The dependencies get installed successfully.
Once installed and when you have the config files you should be able to run:

```
from spotify_rsm import Analysis

analysis_obj = Analysis('analysis_config.yml') # this one 
analysis_obj.load_data()

analysis_output = analysis_obj.compute_analysis()
print(analysis_output)

analysis_figure = analysis_obj.plot_data()
```

Alternatively, The `.tar.gz`  is part of the repository. 

## Inspiration
This repo is based on items learned during Building Software section of cohort 2 of DSI. 
Inspired by Simeon Wong, who inadvertantly taught us to push ourselves forward and read a lot of documentation on the way.
