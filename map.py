from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import re

df = pd.read_csv('data_states.csv')

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
    Input("my-radio-buttons", "value"))
def display_map(candidate):

    if candidate == 'LDA':
        colorbar_title = "LDA topics"
        data_type = str
    elif candidate == 'NMF':
        colorbar_title = "NMF topics"
        data_type = str
    else : 
        colorbar_title = "Sentiments"
        data_type = float

    fig = px.choropleth(
        locations=df['state'][:-1], 
        locationmode="USA-states", 
        color=df[candidate][:-1].astype(data_type), 
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
    Input("my-map", "hoverData"))
def update_kpi_card(hoover_text):
    text = 'USA'
    value = df['Total'].loc[df['state'] == 'USA']

    if(hoover_text):
        text = df['state_name'].loc[df['state'] == hoover_text['points'][0]['location']]
        value = df['Total'].loc[df['state'] == hoover_text['points'][0]['location']]

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
    Input("my-map", "hoverData"))
def update_bar_chart_words(hoover_text):

    words = df['words'].loc[df['state'] == 'USA'].values[0]
    freq = df['freq'].loc[df['state'] == 'USA'].values[0]

    if hoover_text :
        words = df['words'].loc[df['state'] == hoover_text['points'][0]['location']].values[0]
        freq = df['freq'].loc[df['state'] == hoover_text['points'][0]['location']].values[0]

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
    Input("my-map", "hoverData"))
def update_bar_chart(candidate, hoover_text):

    if candidate == 'LDA':
        columns = ['LDA_0','LDA_1','LDA_2','LDA_3','LDA_4','LDA_5','LDA_6','LDA_7','LDA_8','LDA_9',]
    elif candidate == 'NMF':
        columns = ['NMF_0','NMF_1','NMF_2','NMF_3','NMF_4','NMF_5','NMF_6','NMF_7','NMF_8','NMF_9',]
    else : 
        columns = ['Negative', 'Neutral', 'Positive']

    row = df[columns].loc[df['state'] == 'USA'].values[0]
    range = row.max()

    if(hoover_text):
        row = df[columns].loc[df['state'] == hoover_text['points'][0]['location']].values[0]
        range = df[columns][:-1].max().max()

    fig = go.Figure(data=[
        go.Bar(x=columns, y=row),
    ])

    fig.update_layout(title_text='Répartition', yaxis_range=[0,range])

    return fig


app.run_server(debug=True)