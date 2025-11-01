import pandas as pd
from stocktrends import indicators

def test_get_state():
    """
    Test case where the get_state method of the PnF class is tested. It checks if the method returns the correct state based on the given parameters.
    """
    df = pd.read_csv('unit_samples/HOOLI.csv')
    df.columns = [i.lower() for i in df.columns]
    pnf = indicators.PnF(df)
    assert pnf.get_state(True, 1) == pnf.UPTREND_CONTINUAL
    assert pnf.get_state(True, -3) == pnf.UPTREND_REVERSAL
    assert pnf.get_state(False, -3) == pnf.DOWNTREND_CONTINUAL
    assert pnf.get_state(False, 4) == pnf.DOWNTREND_REVERSAL

def test_roundit():
    """
    Test the roundit method of the PnF class. This function tests the roundit method of the PnF class by asserting the expected results for different inputs.
    """
    df = pd.read_csv('unit_samples/HOOLI.csv')
    df.columns = [i.lower() for i in df.columns]
    pnf = indicators.PnF(df)
    assert pnf.roundit(6) == 5
    assert pnf.roundit(21, base=5) == 20
    assert pnf.roundit(38, base=5) == 40


