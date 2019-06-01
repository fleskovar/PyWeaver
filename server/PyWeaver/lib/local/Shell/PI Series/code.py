from os import sys, path
from datetime import datetime, timedelta

sys.path.append('C:\\Users\\f.leskovar\\PycharmProjects\\STEAM')
from shared.ShellData.PI import PITag
from shared.DataAnalysis.SignalProcessing import Shapes, DataFilter as df


def f():
    start_date = datetime(2019, 5, 19)
    end_date = datetime(2019, 5, 20)

    pi_tag = display['pi_tag']  # Gets value from UI

    alim_tag = PITag(pi_tag)
    x, y, dates = df.GetTimeSeries(alim_tag, start_date, end_date, time_step='10m')

    return x, y