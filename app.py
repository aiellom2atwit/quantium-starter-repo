import dash
from dash import html, dcc, Input, Output
import pandas as pd
import plotly.express as px

# Load the data
df = pd.read_csv('data/output.csv')
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')

app = dash.Dash(__name__)

app.layout = html.Div(style={
    'backgroundColor': '#1a0a2e',
    'minHeight': '100vh',
    'fontFamily': 'Arial, sans-serif',
    'padding': '20px'
}, children=[

    html.H1('Soul Foods Pink Morsel Sales Visualiser', style={
        'color': '#E8339D',
        'textAlign': 'center',
        'fontSize': '2.5em',
        'marginBottom': '10px',
        'textShadow': '0 0 20px #E8339D'
    }),

    html.P('Filter by Region:', style={
        'color': '#9B33E8',
        'textAlign': 'center',
        'fontSize': '1.1em',
        'marginBottom': '5px'
    }),

    dcc.RadioItems(
        id='region-filter',
        options=[
            {'label': 'All', 'value': 'all'},
            {'label': 'North', 'value': 'north'},
            {'label': 'East', 'value': 'east'},
            {'label': 'South', 'value': 'south'},
            {'label': 'West', 'value': 'west'},
        ],
        value='all',
        inline=True,
        style={'textAlign': 'center', 'marginBottom': '20px'},
        labelStyle={
            'color': '#E880BD',
            'marginRight': '20px',
            'fontSize': '1.1em',
            'cursor': 'pointer'
        }
    ),

    dcc.Graph(id='sales-chart')
])

@app.callback(
    Output('sales-chart', 'figure'),
    Input('region-filter', 'value')
)
def update_chart(region):
    if region == 'all':
        filtered = df.groupby('date')['sales'].sum().reset_index()
    else:
        filtered = df[df['region'] == region].groupby('date')['sales'].sum().reset_index()

    fig = px.line(
        filtered,
        x='date',
        y='sales',
        labels={'date': 'Date', 'sales': 'Sales ($)'},
        title=f'Pink Morsel Sales - {region.capitalize()}'
    )

    fig.update_traces(line_color='#E8339D')

    fig.add_shape(
        type='line',
        x0='2021-01-15', x1='2021-01-15',
        y0=0, y1=1,
        yref='paper',
        line=dict(color='#E85433', dash='dash', width=2)
    )

    fig.add_annotation(
        x='2021-01-15',
        y=1,
        yref='paper',
        text='Price Increase',
        showarrow=False,
        xanchor='left',
        font=dict(color='#E85433', size=12)
    )

    fig.update_layout(
        plot_bgcolor='#2d1b4e',
        paper_bgcolor='#1a0a2e',
        font_color='#E880BD',
        title_font_color='#E8339D',
        xaxis=dict(gridcolor='#3d2b5e'),
        yaxis=dict(gridcolor='#3d2b5e')
    )

    return fig

if __name__ == '__main__':
    app.run(debug=True)