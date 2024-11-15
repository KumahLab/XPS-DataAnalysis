#!/usr/bin/env python
# coding: utf-8

import matplotlib.pyplot as plt 
from matplotlib.lines import Line2D
from scipy.signal import lfilter
from scipy.signal import find_peaks
import pandas as pd 
import numpy as np
import math
from ipywidgets import interact


f_02vs10 = {'JS002_firstclean_survey_xps_dat.xlsx': 'JS002',
           'JS010_firstclean_survey_xps_dat.xlsx': 'JS010'}

f_cleaning = {'JS010_firstclean_survey_xps_dat.xlsx': '2 mins sputter',
             'JS010_secondclean_survey_xps_dat.xlsx': '5 mins sputter',
             'JS010_thirdclean_survey_xps_dat.xlsx': '20 mins sputter'}


# ## Important XPS Peaks
ti_3plus = 459
ti_4plus = 458
ox_al2o3 = 531
c_1s = 285


# ## Function to smooth data, scale to carbon peak
def xps_plot(f):
    file = pd.read_excel(f)
    bind_energ = file["Binding Energy (eV)"]
    intens = file['Intensity']
    
    #Smooth data
    n = 5
    b = [1.0/n] * n
    a = 1
    intens_smooth = lfilter(b,a,file['Intensity'])
    
    #Scale data by carbon peak
    peaks, _ = find_peaks(intens_smooth, height = 0.02)
    for p in peaks:
        if bind_energ[p]>=275 and bind_energ[p]<=290: #range for carbon
            c_peak_ind = p
            bind_energ_carbon = bind_energ[c_peak_ind]
            
    dat_shift = c_1s - bind_energ_carbon
    bind_energ_shift = [i+dat_shift for i in bind_energ]
    
    return bind_energ_shift, intens_smooth


# # Ar Sputter Time
import pandas as pd
import plotly.graph_objects as go

a1,b1 = xps_plot('JS010_firstclean_survey_xps_dat.xlsx')
a2,b2 = xps_plot('JS010_secondclean_survey_xps_dat.xlsx')
a3,b3 = xps_plot('JS010_thirdclean_survey_xps_dat.xlsx')
a4,b4 = xps_plot('JS002_firstclean_survey_xps_dat.xlsx')

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=a1,
        y=b1,
        mode="lines",
        name='2 mins sputter',
        line=go.scatter.Line(color='#1f77b4'),
        showlegend=True)
)
fig.add_trace(
    go.Scatter(
        x=a2,
        y=b2,
        mode="lines",
        name='5 mins sputter',
        line=go.scatter.Line(color='#ff7f0e'),
        showlegend=True)
)
fig.add_trace(
    go.Scatter(
        x=a3,
        y=b3,
        mode="lines",
        name='20 mins sputter',
        line=go.scatter.Line(color='#2ca02c'),
        showlegend=True)
)


fig.add_trace(
    go.Scatter(
        x=[c_1s, c_1s],
        y=[-1,1],
        name="Carbon",
        mode='lines',
        line=go.scatter.Line(color='rgb(102,102,102)', width = 1.5, dash='dash')))



fig.update_layout(yaxis_range=[-0.005,0.11])
fig.update_layout(xaxis_range=[0,1000])
fig.update_layout(title='XPS for Increasing Sputter times',
                  xaxis_title="Binding Energy (eV)",
                  yaxis_title="Intensity",
                  legend_title=None)
fig.show()
fig.write_html("/home/jms378/Documents/JS00X_Series_data/JS00X_XPS/XPS_cleaning.html")


# # JS002 vs JS010
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=a3,
        y=b3,
        mode="lines",
        name='JS010 (Ti2O3)',
        line=go.scatter.Line(color='#2ca02c'),
        showlegend=True)
)

fig.add_trace(
    go.Scatter(
        x=a4,
        y=b4,
        mode="lines",
        name='JS002 (Ti3O5)',
        line=go.scatter.Line(color='#9467bd'),
        showlegend=True)
)

fig.add_trace(
    go.Scatter(
        x=[c_1s, c_1s],
        y=[-1,1],
        name="Carbon",
        mode='lines',
        line=go.scatter.Line(color='rgb(102,102,102)', width = 1.5, dash='dash')))

fig.update_layout(yaxis_range=[-0.005,0.11])
fig.update_layout(xaxis_range=[0,1000])
fig.update_layout(title='XPS for JS002 (2 mins sputter) vs JS010 (20 mins sputter)',
                  xaxis_title="Binding Energy (eV)",
                  yaxis_title="Intensity",
                  legend_title=None)
fig.show()

fig.write_html("/home/jms378/Documents/JS00X_Series_data/JS00X_XPS/XPS_JS002vsJS010.html")




