from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import re

df = pd.read_csv('data_map.csv')

fontawesome_stylesheet = "styles.css"

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([

    html.Div(children=[
        html.Div(children=[
            dbc.RadioItems(
                id='my-radio-buttons', 
                options=[
                    {"label": "Sentiments analysis", "value": "sentiment"},
                    {"label": "Topic model LDA", "value": "LDA"},
                    {"label": "Topic model NMF", "value": "NMF"},
                ],
                value="sentiment",
                inline = True,
                style={'margin-bottom': '70px', 'margin-left': '30px'}
            ),
            dcc.Graph(id="my-map"),
            dcc.Slider(0, 6,
                step=None,
                marks={
                    0: '2020',
                    1: 'janv 2020',
                    2: 'feb 2020',
                    3: 'mar 2020',
                    4: 'apr 2020',
                    5: 'may 2020',
                },
                value=0,
                id='my-slider'
            )

        ],style={'width': '49%', 'display': 'inline-block'}),
        html.Div(children=[
            html.Div(id='my-card', style={'margin-top': '20px'}),
            dcc.Graph(id="my-graph-bar2"),
        ],style={'width': '49%', 'display': 'inline-block'}),
    ]),
    dcc.Graph(id="my-graph-bar"),
])


@app.callback(
    Output("my-map", "figure"), 
    Input("my-radio-buttons", "value"),
    Input('my-slider', 'value'))
def display_map(radio_button_value, slider_value):

    if radio_button_value == 'LDA':
        colorbar_title = "LDA topics"
        data_type = str
    elif radio_button_value == 'NMF':
        colorbar_title = "NMF topics"
        data_type = str
    else : 
        colorbar_title = "Sentiments"
        data_type = float

    fig = px.choropleth(
        locations=df['state'].loc[df['month'] == slider_value], 
        locationmode="USA-states", 
        color=df[radio_button_value].loc[df['month'] == slider_value].astype(data_type), 
        color_continuous_scale=["red", "yellow", "green"],
        color_discrete_sequence=px.colors.qualitative.G10,
        scope="usa",
    )

    fig.update_layout(
        title_text = colorbar_title + ' by states',
        geo_scope='usa',
        coloraxis_colorbar_title_text = colorbar_title,
    )

    return fig


@app.callback(
    Output('my-card', 'children'),
    Input("my-map", "hoverData"),
    Input('my-slider', 'value'))
def update_kpi_card(hoover_text, slider_value):
    
    text = 'USA'
    value = df['Total'].loc[(df['state'] == 'USA') & (df['month'] == slider_value)]

    if(hoover_text):
        state_selected = hoover_text['points'][0]['location']
        text = df['state_name'].loc[(df['state'] == state_selected) & (df['month'] == slider_value)]
        value = df['Total'].loc[(df['state'] == state_selected) & (df['month'] == slider_value)]

    card = dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H4(text),
                    html.P(value)
                ]
            ),
        ],
        style={'margin-left': 'auto', 'margin-right': 'auto', 'width': '40%','text-align':'center'},
    )

    return card



@app.callback(
    Output("my-graph-bar2", "figure"),
    Input("my-map", "hoverData"),
    Input('my-slider', 'value'))
def update_bar_chart_words(hoover_text, slider_value):

    words = df['words'].loc[(df['state'] == 'USA') & (df['month'] == slider_value)].values[0]
    freq = df['freq'].loc[(df['state'] == 'USA') & (df['month'] == slider_value)].values[0]

    if hoover_text :
        state_selected = hoover_text['points'][0]['location']
        words = df['words'].loc[(df['state'] == state_selected) & (df['month'] == slider_value)].values[0]
        freq = df['freq'].loc[(df['state'] == state_selected) & (df['month'] == slider_value)].values[0]

    # nettoyer les listes 
    words = re.sub('\n','',words)
    words = re.sub("'",'',words)
    words = words.strip('][').split(' ')
    
    freq = re.sub('\n','',freq)
    freq = re.sub('\s+',' ',freq)
    freq = re.sub('\s+]','',freq)
    freq = freq.strip('][').split(' ') 
    freq = [int(i) for i in freq]


    fig = go.Figure(data=[
        go.Bar(x=freq[::-1], y=words[::-1], orientation='h'),
    ])

    fig.update_layout(title_text='Top words')

    return fig
        

@app.callback(
    Output("my-graph-bar", "figure"),
    Input("my-radio-buttons", "value"),
    Input("my-map", "hoverData"),
    Input('my-slider', 'value'))
def update_bar_chart(radio_button_value, hoover_text, slider_value):

    if radio_button_value == 'LDA':
        columns = ['LDA_0','LDA_1','LDA_2','LDA_3','LDA_4','LDA_5','LDA_6','LDA_7','LDA_8','LDA_9',]
    elif radio_button_value == 'NMF':
        columns = ['NMF_0','NMF_1','NMF_2','NMF_3','NMF_4','NMF_5','NMF_6','NMF_7','NMF_8','NMF_9',]
    else : 
        columns = ['Negative', 'Neutral', 'Positive']

    row = df[columns].loc[(df['state'] == 'USA') & (df['month'] == slider_value)].values[0]

    if(hoover_text):
        state_selected = hoover_text['points'][0]['location']
        row = df[columns].loc[(df['state'] == state_selected) & (df['month'] == slider_value)].values[0]

    fig = go.Figure(data=[
        go.Bar(x=columns, y=row),
    ])

    fig.update_layout(title_text='Repartition')

    return fig


app.run_server(debug=True)