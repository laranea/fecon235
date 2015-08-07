#  Python Module for import                           Date : 2015-02-05
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per Python PEP 0263 
''' 
_______________|  yi_quandl.py : Access Quandl with pandas for plots, etc.

We define procedures to access data from Quandl.  Each economic time series
and its frequency has its own "quandlcode" which is available at their site:
http://www.quandl.com

          Usage:  df = getqdl( quandlcode )
                  #            ^Favorites are named d4*, w4*, m4*, q4*.

                  plotqdl( dataframe or quandlcode )

                  holtqdl( dataframe or quandlcode )
                  #  Holt-Winters forecast.

                  #  Single column dot notation for quandlcode: 
                  #  e.g. 'NSE/OIL.4' grabs the 4th column of NSE/OIL.

SYNOPSIS
          _____ API Key

You will need an API Key unless you are doing fewer than 50 calls per day.

Once you have your token, simply include it with your first function call,
like this:

     mydata = qdlapi.get("NSE/OIL", authtoken="your token here")

It will then be stored in your working directory for continued use.
Authtokens are saved as pickled files in the local directory as "authtoken.p"
so it is unnecessary to enter them more than once, unless you change your
working directory. 

After creating an account at quandl.com, set your authentication token with
the [Deprecated: Quandl.auth() function] setQuandlToken function below.


          _____ Usage Rules

API usage is free for registered users. Registered users have a limit of 2,000
calls per 10 minutes, and a limit of 50,000 calls per day. Premium data
subscribers have a limit of 5,000 calls per 10 minutes, and a limit of 720,000
calls per day.  Dataset calls are rate-limited to 2,000 calls per 10 minutes.

All API requests must be made using HTTPS. Requests made over HTTP will fail.


          _____ Quandl Codes

To use the API to download a dataset, you will need to know the dataset's
"quandlcode".  Each dataset on Quandl has a unique Quandl code, comprising a
database_code and a dataset_code. For instance, the dataset named GDP of the
United States has the Quandl code FRED/GDP, where FRED is the database code
and GDP is the dataset_code. All datasets from the same database will have the
same database code.

Dataset codes are not guaranteed to be unique across databases. SHFE/CUG2014
is not the same as MCX/CUG2014. You need both the database_code and the
dataset_code to fully identify a dataset.


          _____ Pre-calculations

In general, we suggest downloading the data in raw format in the highest
frequency possible and preforming any data manipulation in pandas itself.

Quandl allows you to perform certain elementary calculations on your data
prior to downloading. The transformations currently availabe are row-on-row
change, percentage change, cumulative sum, and normalize (set starting value
at 100).  If a datapoint for time t is denoted as y[t] and the transformed
data as y'[t], the available transformations are defined as below:

Transformation      Parameter     Effect
Row-on-row change   diff          y'[t] = y[t] - y[t-1]
Row-on-row % change rdiff         y'[t] = (y[t] - y[t-1])/y[t-1]
Cumulative sum      cumul         y'[t] = y[t] +y[t-1] + ... + y[0]
Start at 100        normalize     y'[t] = (y[t]/y[0]) * 100

Note that y[0] in the above table refers to the starting date for the API
call, i.e., the date specified by trim_start= or rows=, NOT the starting date
of the entire dataset.


          _____ Specific API Guides

Economics: https://www.quandl.com/resources/api-for-economic-data
Stocks:    https://www.quandl.com/resources/api-for-stock-data
Earnings:  https://www.quandl.com/resources/api-for-earnings-data
Futures:   https://www.quandl.com/resources/api-for-futures-data
Currencies:  https://www.quandl.com/resources/api-for-currency-data
Bitcoin:     https://www.quandl.com/resources/api-for-bitcoin-data
Commodities: https://www.quandl.com/resources/api-for-commodity-data
Housing:     https://www.quandl.com/resources/api-for-housing-data
Cross-Country Stats: https://www.quandl.com/resources/api-for-country-data


          _____ Contact

Reach out to Quandl for direct support at connect@quandl.com
Inquires about the Python API package to    Chris@quandl.com


     __________ Using Quandl's Python module

[We have copied the Quandl.py module to yi_quandl_api.py as qdlapi. 
 Thus their use of Quandl.get is equivalent to our quandl function here.]

The Quandl package is able to return data in 2 formats: a pandas data series
("pandas") and a numpy array ("numpy"). "pandas" is the default. Here's how
you specify the format explicitly:

     mydata = Quandl.get("WIKI/AAPL", returns="numpy")

You can get multiple datasets in one call by passing an array of Quandl codes,
like this:

     mydata = Quandl.get(["NSE/OIL.4","WIKI/AAPL.1"])

This grabs the 4th column of dataset NSE/OIL and the 1st column of dataset
WIKI/AAPL, and returns them in a single call.

Python package offers various ways to manipulate or transform the data prior
to download: 

     Specific Date Range:
     mydata = Quandl.get("NSE/OIL", trim_start="yyyy-mm-dd", 
                                    trim_end="yyyy-mm-dd")

     Frequency Change:
     mydata = Quandl.get("NSE/OIL", collapse="annual")
     #  ("daily"|weekly"|"monthly"|"quarterly"|"annual")

     Transformations:
     mydata = Quandl.get("NSE/OIL", transformation="rdiff")
     #  ("diff"|"rdiff"|"normalize"|"cumul")

     Return last n rows:
     mydata = Quandl.get("NSE/OIL", rows=5)

A request with a full list of options would look like the following:

data = Quandl.get('PRAGUESE/PX', authtoken='xxxxxx', trim_start='2001-01-01',
                  trim_end='2010-01-01', collapse='annual',
                  transformation='rdiff', rows=4, returns='numpy')


          _____ Push Example

You can now upload your own data to Quandl through the Python package. At this
time the only accepted format is a date indexed Pandas DataSeries.

Things to do before you upload:

    - Make an account and set your authentication token within the package
      with the setQuandlToken function below.
    - Get your data into a data frame with the dates in the first column.
    - Pick a code for your dataset - only capital letters, numbers and
      underscores are acceptable.

Then call the following to push the data:
     Quandl.push(data, code='TEST', name='Test', desc='test')

All parameters but desc are necessary. If you wish to override the existing
set at code TEST add override=True.


REFERENCES:

- Using Quandl's Python module: https://www.quandl.com/help/python
                   GitHub repo: https://github.com/quandl/quandl-python

- Complete Quandl API documentation: https://www.quandl.com/docs/api
  including error codes.

- [ RESTful interface introduction:  https://www.quandl.com/help/api
            Not needed here, but it's available. ]

- CFTC Commitments of Traders Report, explanatory notes:
  http://www.cftc.gov/MarketReports/CommitmentsofTraders/ExplanatoryNotes

     - Traders' option positions are computed on a futures-equivalent basis
       using delta factors supplied by the exchanges.
     
- Computational tools for pandas
       http://pandas.pydata.org/pandas-docs/stable/computation.html

- Wes McKinney, 2013, _Python for Data Analysis_.


CHANGE LOG  For latest version, see https://github.com/rsvp/fecon235
2015-08-03  First version patterned after yi_fred.py
'''


import pandas as pd               #  for data munging.
import yi_quandl_api as qdlapi    #  a.k.a. Quandl.py module

import yi_1tools as tools         #  Our tools.
import yi_fred as fred            #  For: plotdf
import yi_timeseries as ts        #  esp. Holt-Winters.



#      __________ Convenient ABBREVIATIONS for less typing of quotes:
#                 pandas can use string to slice data, e.g. df[t06:]
t50    = '1950'
t60    = '1960'
t70    = '1970'
t80    = '1980'
t90    = '1990'
t98    = '1998'
t00    = '2000'
t06    = '2006'                  #  a.k.a. post Great Recession.
t10    = '2010'
t13    = '2013'

T      = 'T'                     #  Generic time index.
Y      = 'Y'                     #  GENERIC FIRST COLUMN name herein.
y      = 'Y'                     #  GENERIC FIRST COLUMN name herein.



#      __________ FUTURES quandlcode:
f4treasury10  = 'TY'             #  CBOT
f4fedfunds    = 'FF'             #  CBOT
f4eurodollars = 'ED'             #  CME
f4spx         = 'SP'             #  CME
f4spmini      = 'ES'             #  CME
f4eur         = 'EC'             #  CME
f4chf         = 'SF'             #  CME
f4gbp         = 'BP'             #  CME
f4jpy         = 'JY'             #  CME
f4cad         = 'CD'             #  CME
f4xau         = 'GC'             #  COMEX
f4oilwti      = 'CL'             #  NYMEX



#      __________ WEEKLY quandlcode:
w4cotr_xau      = 'w4cotr_xau'      #  CFTC COTR Manager position: Gold
w4cotr_usd      = 'w4cotr_usd'      #  CFTC COTR Manager position: US Dollar
w4cotr_bonds    = 'w4cotr_bonds'    #  CFTC COTR Manager position: Bonds
w4cotr_equities = 'w4cotr_equities' #  CFTC COTR Manager position: Equities



#       __________ ALIASES

quandl = qdlapi.get
#              ^MAIN workhorse to RETREIVE data using QUANDL API.
#                    Note: getqdl is our convenience wrapper.



def setQuandlToken( API_key ):
     '''Generate authtoken.p in the local directory for API access.'''
     #  Must have API key which is free by creating a Quandl account, 
     #  however, this is not necessary for very limited usage.
     dummy = qdlapi.get("NSE/OIL", authtoken=API_key, rows=1)
     #  The first request is all that matters for getting initiated.
     print ' ::  Generated authtoken.p in local directory for API access.'
     #
     #  For security, authtoken.p shall not be committed via .gitignore


def cotr_get( futures='GC', type='FO' ):
     '''Get CFTC Commitment of Traders Report COTR.'''
     #  Report for futures only requested by type "F".
     #  Report for both futures and options requested by type "FO".
     #  e.g. 'CFTC/GC_FO_ALL' for CFTC COTR: Gold futures and options.
     #
     #  Traders' option positions are computed on a futures-equivalent basis
     #  using delta factors supplied by the exchanges.
     quandlcode = 'CFTC/' + futures + '_' + type + '_ALL'
     return quandl( quandlcode )


def cotr_position( futures='GC' ):
     '''Extract market position from CFTC Commitment of Traders Report.'''
     cotr = cotr_get( futures )
     #  Report for both futures and options requested by implicit "FO".
     #
     #  For directionality we use these categories:
     try:
          longs  = cotr['Asset Manager Longs']
          shorts = cotr['Asset Manager Shorts']
          #  "Leveraged Funds" for FINANCIALS appear short-term, whereas 
          #  "Asset Manager" takes longer term perspective.
     except:
          longs  = cotr['Money Manager Longs']
          shorts = cotr['Money Manager Shorts']
          #  "Money Manager" for COMMODITIES. 
          #  The report is structured differently than financials.
          #
     #                _Scale-free between 0 and 1 indicating bullishness.
     return tools.todf( longs / (longs + shorts ))


def cotr_position_usd():
     '''Market position for USD from COTR of JY and EC.'''
     #  We ignore USD index DX from ICE.
     pos1 = cotr_position( 'JY' )
     #                      JPY futures.
     pos2 = cotr_position( 'EC' )
     #                      EUR futures.
     #
     #                  _Inverts position relative to quotation styles.
     #                      _Average reading between two contracts.
     return tools.todf( 1 - ((pos1 + pos2) / 2.0) )


def cotr_position_bonds():
     '''Market position for bonds from COTR of TY and ED.'''
     pos1 = cotr_position( 'TY' )
     #                      TY is 10-years.
     pos2 = cotr_position( 'ED' )
     #                      Eurodollar strips.
     #
     #                  _Average reading between two contracts.
     return tools.todf( (pos1 + pos2) / 2.0 )


def cotr_position_equities():
     '''Market position for equities from COTR of both SP and ES.'''
     pos1 = cotr_position( 'SP' )
     #                      SP better for options reading.
     pos2 = cotr_position( 'ES' )
     #                      Minis better for reading futures.
     #
     #                  _Average reading between two contracts.
     return tools.todf( (pos1 + pos2) / 2.0 )




def getqdl( quandlcode, maxi=87654321 ):
     '''Retrieve from Quandl in dataframe format, INCL. SPECIAL CASES.'''
     #    maxi is just arbitrarily large as default, 
     #         useful to limit data to last maxi rows, 
     #         e.g. maxi=1 for most recent row only,
     #         but NOT used in all cases below.
     #    We can SYNTHESIZE a quandlcode by use of string equivalent arg:
     if   quandlcode == w4cotr_xau:
          df = cotr_position( f4xau )
     elif quandlcode == w4cotr_usd:
          df = cotr_position_usd()
     elif quandlcode == w4cotr_bonds:
          df = cotr_position_bonds()
     elif quandlcode == w4cotr_equities:
          df = cotr_position_equities()

     else:
          df = quandl( quandlcode, rows=maxi )
     #                 ^just the vanilla series... so
     #                  for "transformation" and "collapse" (resampling), 
     #                  call quandl() directly.
     #
     #         NO NULLS finally, esp. for synthetics derived from 
     #         overlapping indexes, noting that in general: 
     #         readfile does fillna with pad beforehand.
     return df.dropna()



def plotqdl( data, title='tmp', maxi=87654321 ):
     '''Plot data should be it given as dataframe or quandlcode.'''
     #  maxi is an arbitrary maximum number of points to be plotted.
     #  Single column dot notation: e.g. 'NSE/OIL.4'
     #                              grabs the 4th column of NSE/OIL.
     if isinstance( data, pd.DataFrame ):
          fred.plotdf( tools.tail( data, maxi ), title )
     else:
          quandlcode = data
          df = getqdl( quandlcode )
          fred.plotdf( tools.tail( df,   maxi ), title )
     return


def holtqdl( data, h=24, alpha=ts.hw_alpha, beta=ts.hw_beta ):
     '''Holt-Winters forecast h-periods ahead (quandlcode aware).'''
     #  "data" can be a quandlcode, or a dataframe to be detected:
     if isinstance( data, pd.DataFrame ):
          holtdf = ts.holt(  data             , alpha, beta )
     else:
          quandlcode = data
          holtdf = ts.holt( getqdl(quandlcode), alpha, beta )
          #              ^No interim results retained.
     #    holtdf is expensive to compute, but also not retained.
     #    For details, see module yi_timeseries.
     return ts.holtforecast( holtdf, h )





#  #  ======================================== yi_fred.py module =============
#  
#  
#  #  For details on frequency conversion, see McKinney 2103, 
#  #       Chp. 10 Resampling, esp. Table 10-5 on downsampling.
#  #       pandas defaults are:
#  #            how='mean', closed='right', label='right'
#  #
#  #  2014-08-10  closed and label to the 'left' conform to FRED practices.
#  #              how='median' since it is more robust than 'mean'. 
#  #  2014-08-14  If upsampling, interpolate() does linear evenly, 
#  #              disregarding uneven time intervals.
#  
#  
#  def daily( dataframe ):
#       '''Resample data to daily using only business days.'''
#       #                         'D' is used calendar daily
#       #                          B  for business daily
#       df =   dataframe.resample('B', how='median', 
#                                      closed='left', label='left', 
#                                      fill_method=None)
#       #       how= for downsampling, fill_method= for upsampling.
#       return df.interpolate(method='linear')
#       #         ^applies to nulls, if upsampling.
#  
#  
#  def monthly( dataframe ):
#       '''Resample data to FRED's month start frequency.'''
#       #  FRED uses the start of the month to index its monthly data.
#       #                         'M' is used for end of month.
#       #                          MS for start of month.
#       df =   dataframe.resample('MS', how='median', 
#                                       closed='left', label='left', 
#                                       fill_method=None)
#       #        how= for downsampling, fill_method= for upsampling.
#       return df.interpolate(method='linear')
#       #         ^applies to nulls, if upsampling.
#  
#  
#  def quarterly( dataframe ):
#       '''Resample data to FRED's quarterly start frequency.'''
#       #  FRED uses the start of the month to index its monthly data.
#       #  Then for quarterly data: 1-01, 4-01, 7-01, 10-01.
#       #                            Q1    Q2    Q3     Q4
#       #
#       #                          ______Start at first of months,
#       #                          ______for year ending in indicated month.
#       df =   dataframe.resample('QS-OCT', how='median', 
#                                           closed='left', label='left', 
#                                           fill_method=None)
#       #            how= for downsampling, fill_method= for upsampling.
#       return df.interpolate(method='linear')
#       #         ^applies to nulls, if upsampling.
#  
#  
#  
#  def getm4eurusd( fredcode=d4eurusd ):
#       '''Make monthly EURUSD, and try to prepend 1971-2002 archive.'''
#       #  Synthetic euro is the average between 
#       #                 DEM fixed at 1.95583 and 
#       #                 FRF fixed at 6.55957.
#       eurnow = monthly( getdata_fred( fredcode ) )
#       try:
#            eurold = readfile( 'FRED-EURUSD_1971-2002-ARC.csv.gz', compress='gzip' )
#            eurall = eurold.combine_first( eurnow )
#            #               ^appends dataframe
#            print ' ::  EURUSD synthetically goes back monthly to 1971.'
#       except:
#            eurall = eurnow
#            print ' ::  EURUSD monthly without synthetic 1971-2002 archive.'
#       return eurall
#  
#  
    


#  #      __________ save and load dataframe by pickle. 
#                    ^^^^     ^^^^ renamed recently.
#  
#  The easiest way is to pickle it using save:
#  
#       df.to_pickle(file_name)  # where to save it, usually as a .pkl
#  
#  Then you can load it back using:
#  
#       df = pd.read_pickle(file_name)
#
#  However, PICKLE FORMAT IS NOT GUARANTEED, and takes up 4x relative to gz.



if __name__ == "__main__":
     print "\n ::  THIS IS A MODULE for import -- not for direct execution! \n"
     raw_input('Enter something to get out: ')
