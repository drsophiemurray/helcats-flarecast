'''
Contact:
--------
sophie.murray@tcd.ie

Last Update:
------------
2017 December 19

Python Version:
---------------
Python 3.6.1 |Anaconda custom (x86_64)| (default, May 11 2017, 13:04:09)
[GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.57)] on darwin

Description:
------------
Code used to create Figures 3, 6, and 7 as well as histograms (Figures 4, 5, 10, and 11) in HELCATS-FLARECAST paper.

Notes:
------
The lowcat.sav file used is available at https://figshare.com/articles/HELCATS_LOWCAT/4970222
The FLARECAST data is freely available via the flarecast.eu API
Plotly was further used to create the figures as presented in the paper

'''

CAT_FOLDER = '/Users/sophie/Dropbox/lowcat/results/'
LOWCAT_FILE = 'lowcat.sav'
FLARECAST_FILE = 'flarecast_list.csv'

import numpy as np
import datetime as dt
from scipy.io.idl import readsav
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import plotly.graph_objs as go
import plotly.plotly as py
from plotly import tools
import cufflinks as cf

mpl.rc('font', size = 10, family = 'serif', weight='normal')
mpl.rc('legend', fontsize = 8)
mpl.rc('lines', linewidth = 1.5)

def main():
    """Loads the LOWCAT catalogue,
    fixes some data formats,
    then starts creating the plots for the paper"""
    # Load the .sav file
    savfile = readsav(CAT_FOLDER + LOWCAT_FILE)

    # Fix some of the data into a format that is more suitable
    outstr = fix_data(savfile['outstr'])
    df = pd.DataFrame(outstr)

    # Calculate flare duration
    df['FL_DURATION'] = calculate_flare_duration(df['FL_STARTTIME'], df['FL_ENDTIME'])
    df['COR2_TS'] = pd.to_datetime(df['COR2_TS'], format='%d-%b-%Y %H:%M:%S.%f')
    df['COR2_TF'] = pd.to_datetime(df['COR2_TF'], format='%d-%b-%Y %H:%M:%S.%f')
    df['COR2_DURATION'] = calculate_flare_duration(df['COR2_TS'], df['COR2_TF'])

    # Load Jordan's FLARECAST data
    csvdata = pd.read_csv(CAT_FOLDER + FLARECAST_FILE)

    # Create Appendix histograms
    cf.set_config_file(offline=False, world_readable=True, theme='pearl')

    # CME and flare properties
    df['FL_GOES'] = np.log10(df['FL_GOES'].astype('float64'))
    df_cme_hists = df[['COR2_WIDTH', 'COR2_V',
                       'FL_GOES', 'FL_DURATION']]
    df_cme_hists.iplot(kind='histogram', subplots=True, shape=(2, 2),
                       filename='cmeflare_hist',
                       histnorm='percent')

    # SMART properties
    df_smart_hists = df[['SMART_TOTAREA', 'SMART_TOTFLX',
                         'SMART_BMIN', 'SMART_BMAX',
                         'SMART_PSLLEN', 'SMART_BIPOLESEP',
                         'SMART_RVALUE', 'SMART_WLSG']]
    df_smart_hists.iplot(kind='histogram', subplots=True, shape=(4, 2),
                         filename='smart_hist',
                         histnorm='percent')

    # SHARP properties
    df_flarecast_hists_sharp = csvdata[['total (FC data.sharp kw.usiz)', 'max (FC data.sharp kw.usiz)',
                                        'ave (FC data.sharp kw.ushz)', 'max (FC data.sharp kw.ushz)',
                                        'total (FC data.sharp kw.usflux)', 'max (FC data.sharp kw.jz)',
                                        'max (FC data.sharp kw.hgradbh)']]
    df_flarecast_hists_sharp.iplot(kind='histogram', subplots=True, shape=(4, 2),
                                   filename='fcast_hist_final_sharp',
                                   histnorm='percent')

    # Other FLARECAST properties
    df_flarecast_hists = csvdata[['Value Int', 'R Value Br Logr',
                                  'Ising Energy', 'Abs Tot Dedt',
                                  'Tot L Over Hmin', 'Alpha']]
    df_flarecast_hists.iplot(kind='histogram', subplots=True, shape=(3, 2),
                             filename='fcast_hist_final0',
                             histnorm='percent')


    # Figure 4: SRS area vs GOES flux with Hale Class
    srs_area_complexity(df=df)

    # Figure 5 top: GOES flux and WLSG vs CME speed. Colourbar shows angular width (halo)
    plotly_double(x1data = np.log10(df['FL_GOES'].astype('float64')),  x1title = 'GOES Flux [Wm-2]',
                  x2data = df['SMART_WLSG'].astype('float64'), x2title='WLsg [G/Mm]',
                  y1data = df['COR2_V'].astype('float64'), y1title = 'CME Speed [ms<sup>-1</sup>]',
                  y1range = [0., 2000.],
                  weightdata = '10',
                  colourdata = df['COR2_WIDTH'].astype('float64'), colourdata_title='CME width [<sup>o</sup>]',
                  colourdata_max=360, colourdata_min=0, colourdata_step=90,
                  filedata = 'halo_cme_properties_new_colorscale',
                  colourscale=[[0, 'rgb(54,50,153)'],
                               [0.25, 'rgb(54,50,153)'],
                               [0.25, 'rgb(17,123,215)'],
                               [0.5, 'rgb(17,123,215)'],
                               [0.5, 'rgb(37,180,167)'],
                               [0.75, 'rgb(37,180,167)'],
                               [0.75, 'rgb(249,210,41)'],
                               [1.0, 'rgb(249,210,41)']]
                  ) #'Viridis'

    # Figure 5 bottom: Bmin.max, Total area and flux, PSL length, and R value vs CME speed. Colours show flare class.
    plotly_multi(x1data = np.log10(np.abs(df['SMART_BMIN'].astype('float64'))),  x1title = 'Bmin [G]',
                 x2data = np.log10(df['SMART_BMAX'].astype('float64')), x2title = 'Bmax [G]',
                 x3data = np.log10(df['SMART_TOTAREA'].astype('float64')), x3title='Total area [m.s.h]',
                 x4data = np.log10(df['SMART_TOTFLX'].astype('float64')), x4title='Total flux [Mx]',
                 x5data = df['SMART_RVALUE'].astype('float64'), x5title='R value [Mx]',
                 x6data = df['SMART_WLSG'].astype('float64'), x6title='WLsg [G/Mm]',
                 y1data = np.log10(df['COR2_V'].astype('float64')), y1title = 'CME Speed [kms<sup>-1</sup>]',
                 y1range = [2, 3.2],
                 weightdata = '10',
                 colourdata = np.log10(df['FL_GOES'].astype('float64')), colourdata_title = 'GOES Flux [Wm-2]',
                 colourdata_max = -3, colourdata_min = -7, colourdata_step = 1,
                 filedata = 'smart_properties_paper_log10',
                 colourscale=[[0, 'rgb(54,50,153)'],
                              [0.25, 'rgb(54,50,153)'],
                              [0.25, 'rgb(17,123,215)'],
                              [0.5, 'rgb(17,123,215)'],
                              [0.5, 'rgb(37,180,167)'],
                              [0.75, 'rgb(37,180,167)'],
                              [0.75, 'rgb(249,210,41)'],
                              [1.0, 'rgb(249,210,41)']]
                 )

def fix_data(outstr):
    """Some data in the catalogue are in an unfortunate format.
    Here they are converted to something useful for plotting purposes"""
    # Define halo event ranges as integers as per the CACTUS database
    outstr["cor2_halo"][np.where(outstr["cor2_width"] < 120. )] = 1.
    outstr["cor2_halo"][np.where(outstr["cor2_width"] > 120.) and np.where(outstr["cor2_width"] > 270.)] = 2.
    outstr["cor2_halo"][np.where(outstr["cor2_width"] > 270.)] = 3.
    outstr["cor2_halo"][np.logical_not(outstr["cor2_width"] > 0.)] = np.nan
    # Convert GOES strings to magnitudes
    for i in range(len(outstr)):
        outstr["fl_goes"][i] = goes_string2mag(outstr["fl_goes"][i])
        # Get log 10 of R value and WLSG
        if (outstr["SMART_RVALUE"][i] > 0.):
            outstr["SMART_RVALUE"][i] = np.log10(outstr["SMART_RVALUE"][i])
        if (outstr["SMART_WLSG"][i] > 0.):
            outstr["SMART_WLSG"][i] = np.log10(outstr["SMART_WLSG"][i])
        # Convert everything else to NaNs
        for j in range(len(outstr[i])):
            if outstr[i][j] == 0:
                outstr[i][j] = np.nan
    # Now get some datetimes
    outstr['FL_STARTTIME'] = get_dates(outstr['FL_STARTTIME'])
    outstr['FL_ENDTIME'] = get_dates(outstr['FL_ENDTIME'])
    outstr['FL_PEAKTIME'] = get_dates(outstr['FL_PEAKTIME'])
    return outstr


def goes_string2mag(goes):
    """Given a string of GOES class, in format 'M5.2',
    convert to a float with correct magnitude in Wm^(-2).
    If just a blank string then outputs a NaN instead.
    """
    # Skip any blank elements
    if (goes == ' ' or goes == ''):
        output = np.nan
    # Grab the GOES class and magnitude then convert
    else:
        goesclass = list(goes)[0]
        mag = float("".join(list(goes)[1:4]))
        #Combine to Wm^-2
        if goesclass == 'A':
            output = mag * 1.0e-8
        elif goesclass == 'B':
            output = mag * 1.0e-7
        elif goesclass == 'C':
            output = mag * 1.0e-6
        elif goesclass == 'M':
            output = mag * 1.0e-5
        elif goesclass == 'X':
            output = mag * 1.0e-4
    return output


def get_dates(data):
    """Get datetime structures for anything that has a time,
    otherwise just add NaNs"""
    for i in range(len(data)):
        if data[i] == ' ':
            data[i]  = float('NaN')
        else:
            data[i] = dt.datetime.strptime(data[i], '%d-%b-%Y %H:%M:%S.%f')
    return data


def calculate_flare_duration(data_start, data_end):
    """Get flare duration in minutes
    """
    data_out = data_end - data_start
    for i in range(len(data_out)):
        try:
            data_out[i] = (data_out[i]).total_seconds()/60.
        except AttributeError:
            continue
    return data_out


def srs_area_complexity(df):
    """
    Plotting SRS area (x-axis) vs GOES Flux (y-axis).
    Colour will indicate the Hale sunspot complexity classification.
    """
    # Set up plot
    sizecircle = 30
    fig, ax2 = plt.subplots(1, 1)
    # Plot different colours for different Hale classes
    alpha = ax2.scatter(x=np.log10((df['SRS_AREA'].loc[df["SRS_HALE"] == 'Alpha']).astype('float64')),
                        y=np.log10((df['FL_GOES'].loc[df["SRS_HALE"] == 'Alpha']).astype('float64')),
                        s=sizecircle, c='black', lw=0)
    beta = ax2.scatter(x=np.log10((df['SRS_AREA'].loc[df["SRS_HALE"] == 'Beta']).astype('float64')),
                       y=np.log10((df['FL_GOES'].loc[df["SRS_HALE"] == 'Beta']).astype('float64')),
                       s=sizecircle, c='darkblue', lw=0)
    bg = ax2.scatter(x=np.log10((df['SRS_AREA'].loc[df["SRS_HALE"] == 'Beta-Gamma']).astype('float64')),
                     y=np.log10((df['FL_GOES'].loc[df["SRS_HALE"] == 'Beta-Gamma']).astype('float64')),
                     s=sizecircle, c='dodgerblue', lw=0)
    bd = ax2.scatter(x=np.log10((df['SRS_AREA'].loc[df["SRS_HALE"] == 'Beta-Delta']).astype('float64')),
                     y=np.log10((df['FL_GOES'].loc[df["SRS_HALE"] == 'Beta-Delta']).astype('float64')),
                     s=sizecircle, c='darkcyan', lw=0)
    bgd = ax2.scatter(x=np.log10((df['SRS_AREA'].loc[df["SRS_HALE"] == 'Beta-Gamma-Delta']).astype('float64')),
                      y=np.log10((df['FL_GOES'].loc[df["SRS_HALE"] == 'Beta-Gamma-Delta']).astype('float64')),
                      s=sizecircle, c='y', lw=0)
    ax2.set_xlabel(r'log10 SRS Area [m.s.h]')
    ax2.set_xlim([0, 4])
    ax2.set_ylim([-8, -2])
    ax2.set_ylabel(r'log10 GOES Flux [Wm$^{-2}$]')
    ax2.legend((alpha, beta, bg, bd, bgd),
               (r'$\alpha$', r'$\beta$', r'$\beta\gamma$', r'$\beta\delta$', r'$\beta\gamma\delta$'))
    # Save figure to local directory
    fig.savefig('goes_srs_area.eps', format='eps', dpi=1200)


def get_plotly_trace(xdata, ydata,
                     weightdata, colourdata, colourdata_title,
                     colourdata_max, colourdata_min, colourdata_step,
                     showscale, colourscale):
    """Get trace for plotly subplot
    """
    return go.Scatter(x=xdata,
                      y=ydata,
                      mode='markers',
                      marker=dict(size=weightdata,
                                  color=colourdata,
                                  colorscale=colourscale,
                                  showscale=showscale,
                                  cauto=False,
                                  cmax=colourdata_max,
                                  cmin=colourdata_min,
                                  colorbar = dict(title=colourdata_title,
                                                  x=1.01,
                                                  y=0.47,
                                                  len=1,
                                                  thickness=25,
                                                  thicknessmode='pixels',
                                                  xpad=10,
                                                  ypad=10,
                                                  dtick=colourdata_step)
                                  )
                      )


def plotly_double(x1data, x1title,
                  x2data, x2title,
                  y1data, y1title, y1range,
                  weightdata,
                  colourdata, colourdata_title,
                  colourdata_max, colourdata_min, colourdata_step,
                  filedata, colourscale):
    """Make multi subplots in plotly
    """
    trace1 = get_plotly_trace(x1data, y1data,
                              weightdata, colourdata, colourdata_title,
                              colourdata_max, colourdata_min, colourdata_step,
                              showscale=True, colourscale=colourscale)
    trace2 = get_plotly_trace(x2data, y1data,
                              weightdata, colourdata, colourdata_title,
                              colourdata_max, colourdata_min, colourdata_step,
                              showscale=False, colourscale=colourscale)
    fig = tools.make_subplots(rows=1, cols=2)
    fig.append_trace(trace1, 1, 1)
    fig.append_trace(trace2, 1, 2)
    fig['layout'].update(showlegend=False,
                         margin=dict(t=20,
                                     b=80,
                                     l=80,
                                     pad=0),
                         font=dict(size=12)
                         )
    fig['layout']['yaxis1'].update(type='linear',
                                   ticks='outside',
                                   title=y1title,
                                   titlefont=dict(size=12),
                                   showgrid=False,
                                   domain=[0.0, 0.4],
                                   autorange=False,
                                   range=y1range
                                   )
    fig['layout']['yaxis2'].update(type='linear',
                                   ticks='outside',
                                   showgrid=False,
                                   showticklabels=False,
                                   domain=[0.0, 0.4],
                                   autorange=False,
                                   range=y1range
                                   )
    fig['layout']['xaxis1'].update(type='linear',
                                   title = x1title,
                                   titlefont=dict(size=12),
                                   ticks = 'outside',
                                   showgrid=False,
                                   domain=[0.15, 0.55]
                                   )
    fig['layout']['xaxis2'].update(type='linear',
                                   title = x2title,
                                   titlefont=dict(size=12),
                                   ticks = 'outside',
                                   showgrid=False,
                                   domain=[0.6, 1.0]
                                   )
    py.iplot(fig, filename=filedata)


def plotly_multi(x1data, x1title,
                 x2data, x2title,
                 x3data, x3title,
                 x4data, x4title,
                 x5data, x5title,
                 x6data, x6title,
                 y1data, y1title, y1range,
                 weightdata,
                 colourdata, colourdata_title,
                 colourdata_max, colourdata_min, colourdata_step,
                 filedata, colourscale):
    """Make multi subplots in plotly
    """
    trace1 = get_plotly_trace(x1data, y1data,
                              weightdata, colourdata, colourdata_title,
                              colourdata_max, colourdata_min, colourdata_step,
                              showscale=True, colourscale=colourscale)
    trace2 = get_plotly_trace(x2data, y1data,
                              weightdata, colourdata, colourdata_title,
                              colourdata_max, colourdata_min, colourdata_step,
                              showscale=False, colourscale=colourscale)
    trace3 = get_plotly_trace(x3data, y1data,
                              weightdata, colourdata, colourdata_title,
                              colourdata_max, colourdata_min, colourdata_step,
                              showscale=False, colourscale=colourscale)
    trace4 = get_plotly_trace(x4data, y1data,
                              weightdata, colourdata, colourdata_title,
                              colourdata_max, colourdata_min, colourdata_step,
                              showscale=False, colourscale=colourscale)
    trace5 = get_plotly_trace(x5data, y1data,
                              weightdata, colourdata, colourdata_title,
                              colourdata_max, colourdata_min, colourdata_step,
                              showscale=False, colourscale=colourscale)
    trace6 = get_plotly_trace(x6data, y1data,
                              weightdata, colourdata, colourdata_title,
                              colourdata_max, colourdata_min, colourdata_step,
                              showscale=False, colourscale=colourscale)
    fig = tools.make_subplots(rows=3, cols=2)
    fig.append_trace(trace1, 1, 1)
    fig.append_trace(trace2, 1, 2)
    fig.append_trace(trace3, 2, 1)
    fig.append_trace(trace4, 2, 2)
    fig.append_trace(trace5, 3, 1)
    fig.append_trace(trace6, 3, 2)
    fig['layout'].update(showlegend=False,
                         margin=dict(t=20,
                                     b=80,
                                     l=80,
                                     pad=0),
                         font=dict(size=12)
                         )
    fig['layout']['yaxis1'].update(type='linear',
                                   ticks='outside',
                                   showgrid=False,
                                   domain=[.7, 0.95],
                                   autorange=False,
                                   range=y1range
                                   )
    fig['layout']['yaxis2'].update(type='linear',
                                   ticks='outside',
                                   showgrid=False,
                                   showticklabels=False,
                                   domain=[0.7, 0.95],
                                   autorange=False,
                                   range=y1range
                                   )
    fig['layout']['yaxis3'].update(type='linear',
                                   ticks='outside',
                                   title=y1title,
                                   titlefont=dict(size=12),
                                   showgrid=False,
                                   domain=[0.35, 0.6],
                                   autorange=False,
                                   range=y1range
                                   )
    fig['layout']['yaxis4'].update(type='linear',
                                   ticks='outside',
                                   showgrid=False,
                                   showticklabels=False,
                                   domain=[0.35, 0.6],
                                   autorange=False,
                                   range=y1range
                                   )
    fig['layout']['yaxis5'].update(type='linear',
                                   ticks='outside',
                                   showgrid=False,
                                   domain=[0., 0.25],
                                   autorange=False,
                                   range=y1range
                                   )
    fig['layout']['yaxis6'].update(type='linear',
                                   ticks='outside',
                                   showgrid=False,
                                   showticklabels=False,
                                   domain=[0., 0.25],
                                   autorange=False,
                                   range=y1range
                                   )
    fig['layout']['xaxis1'].update(type='linear',
                                   title = x1title,
                                   titlefont=dict(size=12),
                                   ticks = 'outside',
                                   showgrid=False,
                                   domain=[0.4, 0.65]
                                   )
    fig['layout']['xaxis2'].update(type='linear',
                                   title = x2title,
                                   titlefont=dict(size=12),
                                   ticks = 'outside',
                                   showgrid=False,
                                   domain=[0.7, 0.95]
                                   )
    fig['layout']['xaxis3'].update(type='linear',
                                   title = x3title,
                                   titlefont=dict(size=12),
                                   ticks = 'outside',
                                   showgrid=False,
                                   domain=[0.4, 0.65]
                                   )
    fig['layout']['xaxis4'].update(type='linear',
                                   title = x4title,
                                   titlefont=dict(size=12),
                                   ticks = 'outside',
                                   showgrid=False,
                                   domain=[0.7, 0.95]
                                   )
    fig['layout']['xaxis5'].update(type='linear',
                                   title = x5title,
                                   titlefont=dict(size=12),
                                   ticks = 'outside',
                                   showgrid=False,
                                   domain=[0.4, 0.65]
                                   )
    fig['layout']['xaxis6'].update(type='linear',
                                   title = x6title,
                                   titlefont=dict(size=12),
                                   ticks = 'outside',
                                   showgrid=False,
                                   domain=[0.7, 0.95]
                                   )
    py.iplot(fig, filename=filedata)


if __name__ == '__main__':
    main()
