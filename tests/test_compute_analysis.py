import pandas as pd
from pytest import raises

df = pd.read_csv('testing_data.csv')

# Sonia's unit test for analysis
def test_compute_analysis():
    from compute_analysis import compute_analysis
    result = compute_analysis()
    assert result['Number of Tracks'] >=0
    assert result['Playlist Duration'] >=0
    assert result['Number of Artists'] >=0

    with raises(TypeError):
        compute_analysis('this is not a pd.DataFrame')
    
