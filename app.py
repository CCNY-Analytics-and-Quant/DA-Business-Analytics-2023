import pathlib
import pandas as pd
import calendar
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.subplots as sp
import plotly.graph_objects as go
from dash import Dash, html, dcc
import os




PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()

external_stylesheets = ['https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap',
                        'https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

server= app.server

df = pd.read_csv(DATA_PATH.joinpath("SQL_output.csv"))
rain = pd.read_csv(DATA_PATH.joinpath("2015_RainFall.csv"))

df.rename(columns={'pizza_type_id': 'pizza_flavor'}, inplace=True) # I think this name is more appropriate


# Splitting the date into month and days
df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.month
df['day'] = df['date'].dt.day
df['day_of_week'] = df['date'].dt.day_name()
day_order = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
df['hour'] = pd.to_datetime(df['time']).dt.hour


# Year doesnt matter since it doesnt change, dropped it

# Create 'order_id' column so we can check for multiple orders within same time
df['order_id'] = df['month'].astype(str) + df['day'].astype(str) + df['time'].astype(str)

# Create 'multiple_orders' column, 1 if the order_id is duplicated, 0 if not
df['multiple_orders'] = df.duplicated('order_id').astype(int)

# Fixing typing errors in 'ingredients' column

df['ingredients'] = df['ingredients'].str.replace(', ', ',') # one space
df['ingredients'] = df['ingredients'].str.replace(',  ', ',') # two spaces after comma

# Perform one-hot encoding on the 'ingredients' column
ingredients_dummies = df['ingredients'].str.get_dummies(',')

# Add the new columns to the original DataFrame
df = pd.concat([df, ingredients_dummies], axis=1)

df = df.drop('ingredients', axis=1)



tabs_styles = {
    'height': '44px',
    'alignItems': 'center',
    'backgroundColor': '#1E1E1E',
    'padding': '6px',
}

tab_style = {
    'backgroundColor': '#121212',  # Non-selected tabs background
    'color': '#FFFFFF',  # Non-selected tabs text color
    'padding': '10px',  # Padding inside tabs
    'border': 'none'  # Remove borders
}

tab_selected_style = {
    'backgroundColor': '#2D2D2D',  # Selected tab background
    'color': '#FFFFFF',  # Selected tab text color
    'padding': '10px',  # Padding inside selected tab
    'borderRadius': '5px'  # Rounded corners for selected tab
}

app.layout = html.Div(style={
    'backgroundColor': '#303030',  # Dark background for the entire app
    'color': '#FFFFFF',  # White text for the entire app
    'fontFamily': '"Roboto", sans-serif',  # Custom Google font
    'margin': '-8px',  # Remove the default browser margin
    'minHeight': '100vh',  # Full view height
    'padding': '20px'  # Padding for the app
}, children=[
    html.H1("Python for Business Analytics - Jean Batista", style={'textAlign': 'center'}),
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Peak Hours', value='tab-1', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Weather Correlation', value='tab-2', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Variety', value='tab-3', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Sizes', value='tab-4', style=tab_style, selected_style=tab_selected_style),
    ], style=tabs_styles),
    html.Div(id='content')
])

# Define the callback to update the content based on the selected tab
@app.callback(
    Output('content', 'children'),
    Input('tabs', 'value')
)

def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.H2('Orders each Hour | Select a Day from the Dropdown', style={'color': '#FFFFFF'}),
            dcc.Dropdown(
                id='day-dropdown',
                options=[{'label': day, 'value': day} for day in day_order],
                value='Sunday',
                style={'backgroundColor': '#121212', 'color': '#FFFFFF'},  # Dropdown background and text color
            ),
            html.Div([
                dcc.Graph(
                    id='heatmap-graph',
                    figure=update_heatmap('Sunday')   
                ) 
            ]) 
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H2('Rainfall and Total Quantity Sold'),
            dcc.Graph(
                id='subplot-graph',
                figure=update_subplot_graph()
            )
        ])
    elif tab == 'tab-3':
        return html.Div([
            html.H2('Pizza Types'),
            html.Label("Select a month:", style={'font-weight': 'bold', 'display': 'block', 'margin-bottom': '5px'}),
            dcc.Slider(
                id='month-slider',
                min=df['month'].min(),
                max=df['month'].max(),
                value=df['month'].min(),
                marks={int(i): {'label': calendar.month_name[i], 'style': {'transform': 'rotate(-45deg)', 'white-space': 'nowrap'}}
       for i in df['month'].unique()},
                step=None,
            ),
            html.Div(
                id='selected-pizza-stats',
                # This will display the selected pizza statistics, add some space below this div
                style={'margin-bottom': '20px'}  # Adjust the space as needed
            ),
            dcc.Graph(
                id='scatterplot',
                # Call the function with the default slider value
                figure=update_scatterplot(df['month'].min()),
                style={'margin-top': '20px'}  # Add space above the graph
            )
        ])
    elif tab == 'tab-4':
        return html.Div([
            html.H2('Pizza Sizes'),
            dcc.Graph(
                id='bar-chart',
                figure=update_bar_chart()
            ),
            dcc.Graph(
                id='pie-chart',
                figure=update_pie_chart()
            )
        ])
    
def style_graph(graph):
    graph.update_layout(
        paper_bgcolor='#303030',  # Dark background for the graph area
        plot_bgcolor='#303030',  # Dark background inside the graph
        font={'color': '#7FDBFF'},  # Light text for graph components
        xaxis=dict(
            showgrid=False,  # Remove x-axis grid lines
            color='#7FDBFF',  # X-axis text color
            showline=True,  # Show the x-axis line
            linewidth=2,  # Width of the x-axis line
            linecolor='#7FDBFF',  # Color of the x-axis line
        ),
        yaxis=dict(
            showgrid=False,  # Remove y-axis grid lines
            color='#7FDBFF',  # Y-axis text color
            showline=True,  # Show the y-axis line
            linewidth=2,  # Width of the y-axis line
            linecolor='#7FDBFF',  # Color of the y-axis line
        ),
        yaxis2=dict(
            showgrid=False,  # Remove second y-axis grid lines
            color='#7FDBFF',  # Second Y-axis text color
            showline=True,  # Show the second y-axis line
            linewidth=2,  # Width of the second y-axis line
            linecolor='#7FDBFF',  # Color of the second y-axis line
            overlaying='y',  # Ensure the second y-axis overlays the first y-axis
            side='right',  # Position the second y-axis on the right
        ),
        margin=dict(l=40, r=40, t=40, b=40),  # Set the margin to prevent cutting off
        legend=dict(
            bgcolor='rgba(0,0,0,0)',  # Transparent legend background
            bordercolor='#7FDBFF',  # Color of the legend border
        )
    )
    return graph


@app.callback(
    Output('heatmap-graph', 'figure'),
    Input('day-dropdown', 'value')
)
def update_heatmap(day):
    filtered_df = df[df['day_of_week'] == day]
    pizza_type_counts = filtered_df['pizza_flavor'].value_counts()
    popular_pizza_types = pizza_type_counts.nlargest(15).index.tolist()
    filtered_df = filtered_df[filtered_df['pizza_flavor'].isin(popular_pizza_types)]
    filtered_df['hour'] = pd.to_numeric(filtered_df['hour'])  # Convert hour column to numeric
    filtered_df = filtered_df.sort_values('hour')  # Sort DataFrame by hour column
    heatmap_fig = px.density_heatmap(filtered_df, x='hour', y='pizza_flavor', z='quantity', color_continuous_scale='RdYlGn')
    heatmap_fig.update_layout(xaxis={'type': 'category'})  

    return style_graph(heatmap_fig)

def update_subplot_graph():
    results = df.groupby('month')['order_id'].count()
    months = list(range(1, 13))
    days_in_month = [calendar.monthrange(2015, month)[1] for month in months]
    adjusted_quantity = results / days_in_month 
    rainfall = rain.groupby('month').sum()

    # Create the subplot fig
    fig = sp.make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=months, y=adjusted_quantity, name='Total Quantity Sold', line=dict(color='green')), secondary_y=False)
    fig.add_trace(go.Scatter(x=months, y=rainfall['rainfall'], name='Rainfall', line=dict(color='#3076ff')), secondary_y=True)
    fig.update_layout(
        xaxis=dict(title='Month', dtick=1),
        yaxis=dict(
            title='Total Quantity Sold',
            titlefont=dict(color='#7FDBFF'), # baby blue
            tickfont=dict(color='#7FDBFF')
        ),
        yaxis2=dict(
            title='Rainfall in inches',
            titlefont=dict(color='#7FDBFF'),# baby blue 
            tickfont=dict(color='#7FDBFF'), 
            anchor='x',
            overlaying='y',
            side='right'
        ),
        legend=dict(x=0, y=1.2, orientation='h')
    )

    return style_graph(fig)

@app.callback(
    Output('scatterplot', 'figure'),
    [Input('month-slider', 'value')]
)
def update_scatterplot(selected_month):
    # Filter DataFrame based on the selected month
    monthly_df = df[df['month'] == selected_month]

    # Aggregate the data to find total quantity and category for each pizza flavor
    flavor_popularity = monthly_df.groupby(['pizza_flavor', 'category'])['quantity'].sum().reset_index()

    # Create scatter plot, color by 'category'
    scatterplot_fig = px.scatter(flavor_popularity, x='pizza_flavor', y='quantity',
                                 color='category',  # Set the color of the circles based on the 'category'
                                 title='Popularity of Pizza Flavors by Category',
                                 labels={'quantity': 'Total Quantity Sold'},
                                 size='quantity',  # Optional: Use the quantity as the size of the scatter plot markers
                                 hover_name='pizza_flavor')  # Optional: Show the pizza flavor name on hover

    # Update layout
    scatterplot_fig.update_layout(xaxis={'categoryorder': 'total descending'})

    return style_graph(scatterplot_fig)


# I have the pie chart to evaluate if XL and XXL are viable options
def update_pie_chart():
    filtered_df = df[df['pizza_flavor'] == 'the_greek']
    size_quantity = filtered_df.groupby('size')['quantity'].sum().reset_index()

    pie_chart_fig = go.Figure(data=go.Pie(labels=size_quantity['size'], values=size_quantity['quantity']))

    pie_chart_fig.update_layout(title='Pizza Sizes Distribution for "The Greek"',
                                showlegend=True)

    return style_graph(pie_chart_fig)

# I've removed the greek, brie carre, big meats, and five cheese because they would represent outlier
# Because of their size options
def update_bar_chart():
    filtered_df_pie = df[df['pizza_flavor'] == 'the_greek']
    filtered_df_bar = df.copy()

    excluded_sizes = ['XL', 'XXL']
    filtered_df_bar = filtered_df_bar[~filtered_df_bar['size'].isin(excluded_sizes)]

    excluded_pizza_types = ['big_meat', 'brie_carre', 'five_cheese']
    filtered_df_bar = filtered_df_bar[~filtered_df_bar['pizza_flavor'].isin(excluded_pizza_types)]

    size_quantity_bar = filtered_df_bar.groupby('size')['quantity'].sum().reset_index().sort_values('quantity')

    bar_chart_fig = go.Figure(data=go.Bar(x=size_quantity_bar['size'], y=size_quantity_bar['quantity']))

    bar_chart_fig.update_layout(title='Orders by Size',
                                xaxis_title='Size',
                                yaxis_title='Total Quantity Sold')

    return style_graph(bar_chart_fig)


if __name__ == '__main__':
    app.run_server()
