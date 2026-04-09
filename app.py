import dash
from dash import html, dcc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the data
df = pd.read_csv('data/output.csv')
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')

# Aggregate sales by date
df_grouped = df.groupby('date')['sales'].sum().reset_index()

# Create the line chart
fig = px.line(
    df_grouped,
    x='date',
    y='sales',
    title='Pink Morsel Sales Over Time',
    labels={'date': 'Date', 'sales': 'Sales ($)'}
)

# Add vertical line for price increase using a shape instead
fig.add_shape(
    type='line',
    x0='2021-01-15', x1='2021-01-15',
    y0=0, y1=1,
    yref='paper',
    line=dict(color='red', dash='dash')
)

fig.add_annotation(
    x='2021-01-15',
    y=1,
    yref='paper',
    text='Price Increase',
    showarrow=False,
    xanchor='left',
    font=dict(color='red')
)

# Build the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Soul Foods Pink Morsel Sales Visualiser'),
    dcc.Graph(figure=fig)
])

if __name__ == '__main__':
    app.run(debug=True)