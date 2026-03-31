import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Initialize the app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div([
    html.H1('User Dashboard'),
    html.Div([
        html.H2('Select a User:'),
        dcc.Dropdown(
            id='user-dropdown',
            options=[
                {'label': 'User 1', 'value': 'user1'},
                {'label': 'User 2', 'value': 'user2'},
                {'label': 'User 3', 'value': 'user3'}
            ],
            value='user1'
        )
    ]),
    html.Div([
        html.H2('Select a Metric:'),
        dcc.Dropdown(
            id='metric-dropdown',
            options=[
                {'label': 'Metric 1', 'value': 'metric1'},
                {'label': 'Metric 2', 'value': 'metric2'},
                {'label': 'Metric 3', 'value': 'metric3'}
            ],
            value='metric1'
        )
    ]),
    dcc.Graph(id='user-graph')
])

# Define the callback function
@app.callback(
    Output('user-graph', 'figure'),
    [Input('user-dropdown', 'value'),
     Input('metric-dropdown', 'value')]
)
def update_graph(selected_user, selected_metric):
    # Simulate data retrieval from a database or API
    data = {
        'user': ['user1', 'user2', 'user3'],
        'metric': ['metric1', 'metric2', 'metric3'],
        'value': [10, 20, 30]
    }
    df = pd.DataFrame(data)
    
    # Filter data based on selected user and metric
    filtered_df = df[(df['user'] == selected_user) & (df['metric'] == selected_metric)]
    
    # Create the plot
    fig = px.bar(filtered_df, x='user', y='value')
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)