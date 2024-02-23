'''Test file for load_data module. Ideally these would be on a different directory (/tests)
But for the interests of time and not knowing how to handle the relative paths, we just put these in the 
src directory.'''

from pytest import raises

def test_get_playlist_uri():
    from load_data import get_playlist_uri

    input_strings = ['https://open.spotify.com/playlist/4oYSWmdhUMwEu0yAFA47lZ',
                     'https://open.spotify.com/playlist/07BZwq6FrzVKceJx3GMt8n']
    output_strings = ['4oYSWmdhUMwEu0yAFA47lZ','07BZwq6FrzVKceJx3GMt8n']

    for input, output in zip(input_strings, output_strings):
        assert get_playlist_uri(input) == output


def test_get_track_data():
    from load_data import get_track_data

    with raises(TypeError):
        get_track_data('Not a list or dict')


