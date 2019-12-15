# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pds
import plotly.graph_objects as go
import plotly.offline as pyo
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
# import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
pyo.init_notebook_mode()



from database import fetch_all_city_as_df #changed the bpa thing

# Definitions of constants. This projects uses extra CSS stylesheet at `./assets/style.css`
COLORS = ['rgb(67,67,67)', 'rgb(115,115,115)', 'rgb(49,130,189)', 'rgb(189,189,189)']
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', '/assets/style.css']

# Define the dash app first
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# Define component functions


def page_header():
    """
    Returns the page header as a dash `html.Div`
    """
    return html.Div(id='header', children=[
        html.Div([html.H3('Visualization for DATA1050 final project using datashader and Plotly')],
                 className="ten columns"),
        html.A([html.Img(id='logo', src=app.get_asset_url('github.png'),
                         style={'height': '35px', 'paddingTop': '7%'}),
                html.Span('Blownhither', style={'fontSize': '2rem', 'height': '35`px', 'bottom': 0,
                                                'paddingLeft': '4px', 'color': '#a3a7b0',
                                                'textDecoration': 'none'})],
               className="two columns row",
               href='https://github.com/msyed96/1050project'), #change the website here
    ], className="row")


def description(): #about page needs to be seperate page on website but this is all the info in it. 
    """
    Returns overall project description including: project summary, team member names, exec summary, datasets used, summary of 
    performanc wrt baseline & future steps in markdown
    """
    return html.Div(children=[dcc.Markdown('''
        # About Our Project:
        ### Project Summary: 
        How much electricity does Boston City Hall use? Is usage related to the day of the week, the season, or 
        the weather? This project graphs electricity-use data which is posted in fifteen minute increments to reveal 
        trends in how electricity is used in this central municipal building. 
        The visualizations on this page transform data originally published in tabular form into a 
        graphical representation, linked to a separate dataset on daily weather. Using our interactive tool called the Power Predictor! we can 
        explore seasonal trends and see how electricity-use varies. 
        Scroll down to learn more.
        
        ### Boston Power Rangers Team Members:
        - Evon Okidi
        - Marie Schenk
        - Maheen Syed
        - William Ward

        ### References to related work:
        - “Energy Consumption Assessment City of Boston 50 Buildings Report In 2012.”  City of Boston. 
        https://www.cityofboston.gov/images_documents/EEMS%20Energy%20Consumption%20Assessment%20Report%20Final_tcm3-33503.pdf. 
        The city of Boston published an assessment of energy consumption at 50 different buildings, including city hall. 
        These assessments are provided in this journal. 
        - “Boston Energy Use.” ACEEE, American Council for an Energy Efficient Economy, https://database.aceee.org/city/boston-ma. 
        The American Council for an Energy Efficient Economy ranks cities based on their energy use policies; Boston ranks number 1. 
        - “Building Energy Reporting and Disclosure Ordinance.” Boston.gov, 17 July 2016,
         https://www.boston.gov/environment-and-energy/building-energy-reporting-and-disclosure-ordinance. 
         The energy use data is published as part of a city ordinance. Information about the program and the data is available here. 
        - Quantifying Changes in Building Electricity Use, With Application to Demand Response - IEEE Journals & Magazine, 
        https://ieeexplore.ieee.org/abstract/document/5772947. A guide for building managers for dealing with electricity load data
        - Yildiz, B., et al. “A Review and Analysis of Regression and Machine Learning Models on Commercial Building Electricity Load Forecasting.” 
        Renewable and Sustainable Energy Reviews, vol. 73, 2017, pp. 1104–1122. 
        https://www.sciencedirect.com/science/article/pii/S1364032117302265 Machine learning in electricity forecasting.

        
        ### Summary of performance with respect to the baseline model(s): Fill in 

        ### Possible Future Steps:
        One possible extension of this project is to incorporate other buildings into the analysis. 
        Boston also publishes data about electricity use at Central Library in Copley Square. 
        This data is posted in five minute increments, even more frequently than the City Hall data, and is updated six times a day. 
        While City Hall is primarily a place for civil servants to work during business hours, the library is primarily intended as a public gathering place. 
        How does electricity usage differ between these two spaces? Are they affected differently by holidays and weekends?
        Are they most active at different times of day? 

        ### Data Source
        Power Predictor! uses data from the city of Boston's open data hub. Read more about it [here](https://data.boston.gov/dataset/city-hall-electricity-usage). 
        **updates every 4 hours** with data from every 15 minutes. 
        The weather data is from the national center for environmental information [NCEI](https://www.ncei.noaa.gov/)
        
        ''', className='eleven columns', style={'paddingLeft': '5%'})], className="row")


def static_stacked_trend_graph(stack=False):
    """
    Returns scatter line plot of all power sources and power load.
    If `stack` is `True`, the 4 power sources are stacked together to show the overall power
    production.
    """
    df2 = pds.read_csv('data/Date_Temp_Data.csv')
    df = fetch_all_city_as_df()
    if df is None:
        return go.Figure()

    sources = ['Total_Demand_KW']
    x = df['DateTime_Measured']
    x1 = df2['Date/Time']
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Scatter(x=x, y=df['Total_Demand_KW'], mode='lines', name='Total_Demand_KW',
                             line={'width': 2, 'color': 'orange'}))
    fig.add_trace(go.Scatter(x=x1, y=df2['TAVG'], mode='lines', name='Temperature',
                             line={'width': 2, 'color': 'blue'}),secondary_y=True)
    title = 'Power consumption Boston with daily temperature'
    if stack:
        title += ' [Stacked]'

    fig.update_layout(template='plotly_dark',
                      title=title,
                      plot_bgcolor='#23272c',
                      paper_bgcolor='#23272c',
                      xaxis_title='Date/Time')
    fig.update_yaxes(title_text="KW", secondary_y=False)
    fig.update_yaxes(title_text="Temp", secondary_y=True)
    return fig
    # fig = go.Figure()
    # for i, s in enumerate(sources):
    #     fig.add_trace(go.Scatter(x=x, y=df[s], mode='lines', name=s,
    #                              line={'width': 2, 'color': COLORS[i]},
    #                              stackgroup='stack' if stack else None))
    # fig.add_trace(go.Scatter(x=x, y=df['Load'], mode='lines', name='Load',
    #                          line={'width': 2, 'color': 'orange'}))
    # title = 'Energy Production & Consumption under BPA Balancing Authority'
    # if stack:
    #     title += ' [Stacked]'
    # fig.update_layout(template='plotly_dark',
    #                   title=title,
    #                   plot_bgcolor='#23272c',
    #                   paper_bgcolor='#23272c',
    #                   yaxis_title='MW',
    #                   xaxis_title='Date/Time')
    # return fig


def what_if_description(): #DESCRIBE THE ENHANCEMENT STUFF: 
    """
    Returns description of "What-If" - the interactive component
    """
    return html.Div(children=[
        dcc.Markdown('''
        ## Power Predictor!
        The Power Prediction tool is a great way to visualize power consumption on temperature. 
        For example,  a business interested in allocating resources would gain a lot of insight by observing power 
        consumption as it highly impacts budgeting models. Using our Power Predictor tool to look at the varying power
        consumption levels for different months and corresponding temperatures, can make this process much smoother for businesses!
        The steps to construct the tool, involved using polynomial regression with 4 degrees of freedom  to create our predictive model. 
        This model  allows us to predict power consumption based on varying the temperature within each specific month (using the sliders provided). 
        As a result,  the projected power consumption for the specified month will be visualized. 
        You can move around the sliders to and try this out  for yourself! 

        ''', className='eleven columns', style={'paddingLeft': '5%'})
    ], className="row")


def what_if_tool(): 
    """
    Returns the What-If tool as a dash `html.Div`. The view is a 8:3 division between
    demand-supply plot and rescale sliders.
    """
    return html.Div(children=[
        html.Div(children=[dcc.Graph(id='what-if-figure')], className='nine columns'),

        html.Div(children=[
            html.H5("Rescale Montly Temp", style={'marginTop': '2rem'}),
            html.Div(children=[
                dcc.Slider(id='temp-scale-slider', min=0.8, max=1.2, step=0.1, value=1.05, className='row',
                           marks={x: str(x) for x in np.arange(0.8, 1.21, 0.1)})
            ], style={'marginTop': '5rem'}),

            html.Div(id='temp-scale-text', style={'marginTop': '1rem'}),

            html.Div(children=[
                dcc.Slider(id='months-slider', min=1, max=12, step=1, value=6,
                           className='row', marks={x: str(x) for x in np.arange(1, 13, 1)})
            ], style={'marginTop': '3rem'}),
            html.Div(id='months-text', style={'marginTop': '1rem'}),
        ], className='three columns', style={'marginLeft': 5, 'marginTop': '10%'}),
    ], className='row eleven columns')

#DESCRIBE FURTHER DETAILS OF PROJECT. supposed to be a seperate page? : Needs to include Additional project details sections
#Additional Project Details: 
# 1. Development Process and Final Technology Stack
#   Explain how you created the site, and the final technology stack used: highlighted stuff is from martins website, reword this stuff 
# 2.Data Acquisition, Caching, ETL Processing, Database Design
#   Describe how the data is accessed, cached and ETL processing steps
#   Describe the Database used (include a schema diagram if appropriate)
# 3. Link to a static version of your ETL_EDA.ipynb notebook, or equivalent web page: Links to viewable versions of your  ETL_EDA.ipynb, Visualization.ipynb 
# 4. Link to a static version of your Enhancement.ipynb notebook, or equivalent web page: Enhancement.ipynb

def architecture_summary(): 
    """
    Returns the text and image of architecture summary of the project.
    """
    return html.Div(children=[
        dcc.Markdown('''
            # Project Architecture
           The data for this website is stored in a MongoDB database. Queries are performed via function call. 
           The website is hosted through a dash app, and interactive visualizations were prepared using plot.ly. 
           The interactive aspects of the page are redirected through app.py for updates to the page. 


        ''', className='row eleven columns', style={'paddingLeft': '5%'}),

        html.Div(children=[
            html.Img(src="https://docs.google.com/drawings/d/e/2PACX-1vQNerIIsLZU2zMdRhIl3ZZkDMIt7jhE_fjZ6ZxhnJ9bKe1emPcjI92lT5L7aZRYVhJgPZ7EURN0AqRh/pub?w=670&amp;h=457",
                     className='row'),
        ], className='row', style={'textAlign': 'center'}),

        dcc.Markdown('''
        
        ''')
    ], className='row')

# Sequentially add page components to the app's layout

app.layout = html.Div([
    page_header(),
    html.Hr(),
    description(),
    dcc.Graph(id='stacked-trend-graph', figure=static_stacked_trend_graph(stack=False)),
    what_if_description(),
    what_if_tool(),
    architecture_summary(),
    # dcc.Graph(id='what-if-figure', figure=what_if_handler(months, scaler)),
], className='row', id='content')


# Defines the dependencies of interactive components

@app.callback(
    dash.dependencies.Output('temp-scale-text', 'children'),
    [dash.dependencies.Input('temp-scale-slider', 'value')])
def update_temp_scale_text(value):
    """Changes the display text of the temp slider"""
    return "Temperature Scale {:.2f}x".format(value)


@app.callback(
    dash.dependencies.Output('months-text', 'children'),
    [dash.dependencies.Input('months-slider', 'value')])
def update_months_text(value):
    """Changes the display text of the months slider"""
    return "Month Requested {:.2f}x".format(value)


_what_if_data_cache = None


@app.callback(
    dash.dependencies.Output('what-if-figure', 'figure'),
    [dash.dependencies.Input('months-slider', 'value'),
     dash.dependencies.Input('temp-scale-slider', 'value')])
# def what_if_handler(wind, hydro):
#     """Changes the display graph of supply-demand"""
#     df = fetch_all_bpa_as_df(allow_cached=True)
#     x = df['Datetime']
#     supply = df['Wind'] * wind + df['Hydro'] * hydro + df['Fossil/Biomass'] + df['Nuclear']
#     load = df['Load']

#     fig = go.Figure()
#     fig.add_trace(go.Scatter(x=x, y=supply, mode='none', name='supply', line={'width': 2, 'color': 'pink'},
#                   fill='tozeroy'))
#     fig.add_trace(go.Scatter(x=x, y=load, mode='none', name='demand', line={'width': 2, 'color': 'orange'},
#                   fill='tonexty'))
#     fig.update_layout(template='plotly_dark', title='Supply/Demand after Power Scaling',
#                       plot_bgcolor='#23272c', paper_bgcolor='#23272c', yaxis_title='MW',
#                       xaxis_title='Date/Time')
#     return fig

def what_if_handler(months, scaler):
    df2 = pds.read_csv('data/Date_Temp_Data.csv')
    df = fetch_all_city_as_df()
    dates= pds.to_datetime(df['DateTime_Measured'])
    ever2 = pds.concat([dates,df['Total_Demand_KW']],axis = 1,sort = False)
    #monthly_usage = ever2[(ever2['DateTime_Measured'].dt.month ==1) & (ever2['DateTime_Measured'].dt.year == 2018)]
    
    trimonth = pds.DataFrame()
    for x in [2017,2018,2019]:
        monthly_usage = ever2[(ever2['DateTime_Measured'].dt.month ==months) & (ever2['DateTime_Measured'].dt.year == x)]
        temp=monthly_usage.resample('D', on='DateTime_Measured').mean()
        trimonth=pds.concat([trimonth,temp],sort = False)
    dates= pds.to_datetime(df2['Date/Time'])
    ever = pds.concat([dates,df2['TAVG']],axis = 1,sort = False)
    monthly_temp = ever[(ever['Date/Time'].dt.month ==8 )]
    monthly_temp.reset_index(drop = True, inplace = True)
    trimonth.reset_index(drop= True, inplace = True)
    combined_df = pds.concat([monthly_temp['TAVG'],trimonth['Total_Demand_KW']],axis = 1,sort = False)
#    print(combined_df.head())
    combined_df.dropna(inplace = True)
    X = combined_df['TAVG'].values.reshape(-1, 1)
    y = combined_df['Total_Demand_KW'].values.reshape(-1, 1)
#    print(X.shape,y.shape)
    poly = PolynomialFeatures(degree =4) 
    X_poly = poly.fit_transform(X) 
    poly.fit(X_poly, y) 
    lin2 = LinearRegression() 
    lin2.fit(X_poly, y)
    y_pred = lin2.predict(poly.fit_transform(X))
    # plt.scatter(X, y_pred, color = 'red')
    # plt.scatter(X*scaler, lin2.predict(poly.fit_transform(scaler*X)), color = 'blue') 
    # plt.title('Polynomial Regression') 
    # plt.xlabel('Temperature') 
    # plt.ylabel('Power') 
#    return plt
# Create a trace
#     print(np.array(X),np.array(X).flatten(),X)
#     trace = go.Scatter(
#         x = np.array(X).flatten(),
#         y = np.array(y_pred).flatten(),
#         mode = 'markers'
#     )
    y_pred_scaled = lin2.predict(poly.fit_transform(scaler*X))
    fig = go.Figure()
    title = 'Power consumption Boston with daily temperature'
    fig.add_trace(go.Scatter(x=np.array(X).flatten(), y=np.array(y_pred).flatten(), mode='markers', name='Base Temp'))
    fig.add_trace(go.Scatter(x=np.array(X*scaler).flatten(), y=np.array(y_pred_scaled).flatten(), mode='markers', name='Scaled Temp'))
    fig.update_layout(template='plotly_dark',
                      title=title,
                      plot_bgcolor='#23272c',
                      paper_bgcolor='#23272c',
                      xaxis_title='Temperature')
    # Plot and embed in ipython notebook!
    return fig


if __name__ == '__main__':
    app.run_server(debug=True, port=1050, host='0.0.0.0')