from os import sys, path
from datetime import datetime, timedelta

sys.path.append('C:\\Users\\f.leskovar\\PycharmProjects\\py3')
from PI import PITag
from SignalProcessing import Shapes, DataFilter as df


def f(start_date, end_date):

    pi_tag = display['pi_tag']  # Gets value from UI

    alim_tag = PITag(pi_tag)
    x, y, dates = df.GetTimeSeries(alim_tag, start_date, end_date, time_step='10m', epoch=datetime(2010, 1, 1))

    x = x.flatten()
    y = y.flatten()

    return x, y