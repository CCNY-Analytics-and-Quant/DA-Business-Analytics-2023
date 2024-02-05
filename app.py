import pathlib
import pandas as pd
import calendar
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.subplots as sp
import plotly.graph_objects as go
from dash import Dash, html, dcc
import numpy as np
from plotly.subplots import make_subplots



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
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']
df['hour'] = pd.to_datetime(df['time']).dt.hour

# Creating order id
df['order_id'] = df['month'].apply(lambda x: str(x).zfill(2)) + df['day'].apply(lambda x: str(x).zfill(2)) + df['time']

# Create 'multiple_orders' column, 1 if the order_id is duplicated, 0 if not
df['multiple_orders'] = df.duplicated('order_id').astype(int)

# Fixing typing errors in 'ingredients' column
df['ingredients'] = df['ingredients'].str.replace(', ', ',') # one space
df['ingredients'] = df['ingredients'].str.replace(',  ', ',') # two spaces after comma

# Perform one-hot encoding on the 'ingredients' column
ingredients_dummies = df['ingredients'].str.get_dummies(',')

# Add the new columns to the original DataFrame
df = pd.concat([df, ingredients_dummies], axis=1)
df = df.drop('ingredients', axis=1) # Drop the OG 'ingredients' column

hourly_sum_quantity = df.groupby(['day_of_week', 'hour'])['quantity'].sum()
hourly_df = hourly_sum_quantity.reset_index(name='Total Orders sold at this hour of this day')
hourly_df['default_employee_count'] = hourly_df['hour'].apply(lambda x: 3 if 10 < x < 20 else 2)
# set the default employee count to 3 between 10am and 8pm, and 2 otherwise
# This is a very simple model, but it's a good starting point
# It used to calculate the difference between the optimized and default employee count


# CSS styles
tabs_styles = {
    'height': '44px',
    'alignItems': 'center',
    'backgroundColor': '#1E1E1E', # dark grey
    'padding': '6px',
}

tab_style = {
    'backgroundColor': '#121212',  # darker grey tab
    'color': '#FFFFFF',  # white text always
    'padding': '10px',  
    'border': 'none'  # Remove borders
}

tab_selected_style = {
    'backgroundColor': '#2D2D2D',  # Selected tab, light grey
    'color': '#7FDBFF',  # changes to blue when selected
    'padding': '10px',  
    'borderRadius': '5px'  # Rounded corners for selected tab
}

app.layout = html.Div(style={
    'backgroundColor': '#303030',  # Dark background always
    'color': '#FFFFFF',  # White text always
    'fontFamily': '"Roboto", sans-serif',  # custom font
    'margin': '-8px',  
    'minHeight': '100vh',  # Full view height
    'padding': '35px'  # Padding everywhere
}, children=[
    html.H1("Python for Business Analytics - Jean Batista", style={'color': '#FFFFFF','textAlign': 'center'}), # center text color white 
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Peak Hours', value='tab-1', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Weather Correlation', value='tab-2', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Variety', value='tab-3', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Sizes', value='tab-4', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='GitHub', value='tab-5', style=tab_style, selected_style=tab_selected_style),
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
            html.H2('Orders each Hour', style={'color': '#FFFFFF'}),
            html.Div(
                'Minimize labor cost by optimizing staffing hours based on peak time intervals for orders.',
                style={
                    'fontSize': '17px',  # slighter smaller than top text size
                    'marginBottom': '20px',  # Space below the sub-text
                    'marginTop': '5px'  # Space above the sub-text
                }
            ),
            dcc.Slider(
                id='day-slider',
                min=0,
                max=6,
                marks={i: day for i, day in enumerate(day_order)},
                value=0,
                step=None,
            ),
            html.Div([
                dcc.Graph(id='heatmap-graph'),
                dcc.Graph(id='employee-area-chart')  # New Graph for Employee Count
            ]),
            html.Div([
            html.H2('Actionable Insights for Optimized Restaurant Success', style={'color': '#FFFFFF'}),
            html.Div([
                dcc.Markdown('''
                    **Key Performance Indicators (KPIs) to Optimize Success:**

                    - Reduce labor costs by 59% (approximately $79,560 annually) by adjusting staffing hours based on demand. 
                    - This optimization results from analyzing peak hours and adjusting the schedule accordingly, moving from an estimated 253 standard hours to 151 optimized hours weekly.
                ''',
                style={'fontSize': '17px', 'color': '#FFFFFF'}
                ),
        ])
        ])
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H2('Rainfall and Total Quantity Sold'),
            dcc.Graph(
                id='subplot-graph',
                figure=update_subplot_graph()
            ),
            html.H2(' Otimized Operating Cost vs. Rainfall'),
            dcc.Graph(
                id='cost-rainfall-graph',
                figure=update_revenue_cost_rainfall_graph()
            ),
            html.Div([
            html.H2('Actionable Insights for Optimized Restaurant Success', style={'color': '#FFFFFF'}),
            html.Div([
                dcc.Markdown('''
                    **Key Performance Indicators (KPIs) to Optimize Success:**

                    - Reduce operating costs by 6% (approximately $30,780 annually) by adjusting operating cost based on weather conditions. 
                    - This optimization results from analyzing weather conditions and adjusting the resource allocation appropiately, resulting in a change from an estimated $503,417 spent per year to $472,637.
                ''',
                style={'fontSize': '17px', 'color': '#FFFFFF'}
                ),
        ])
        ])
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
    elif tab == 'tab-5':
        return html.Div([
            html.H2('Overview', style={'color': '#FFFFFF'}),
            html.P('For more detailed information and to view the source code, please visit the GitHub repository:'),
            dcc.Link('Visit GitHub Repository', href='https://github.com/CCNY-Analytics-and-Quant/DA-Business-Analytics-2023', target='_blank', style={
             'color': '#7FDBFF',
                'fontSize': '20px',
                'display': 'block',
                'textAlign': 'center',
                'marginTop': '20px',
            })
    ])

    
# Creating function that applies same style to all graphs   
def style_graph(graph): 
    graph.update_layout(
        paper_bgcolor='#303030',  # Dark background for the graph area
        plot_bgcolor='#303030',  # Dark background inside the graph
        font={'color': '#7FDBFF'},  # baby blue
        xaxis=dict(
            showgrid=False,  # Remove x-axis grid lines
            color='#7FDBFF',  # Baby blue always
            showline=True, 
            linewidth=2,  
            linecolor='#7FDBFF',  
        ),
        yaxis=dict(
            showgrid=False,  
            color='#7FDBFF',  
            showline=True,  
            linewidth=2,  
            linecolor='#7FDBFF',  
        ),
        yaxis2=dict( # for the second y axis in Weather Correlation
            showgrid=False,  
            color='#7FDBFF',  
            showline=True,  
            linewidth=2,  
            linecolor='#7FDBFF',  
            overlaying='y',  
            side='right',  
        ),
        legend=dict(
            bgcolor='rgba(0,0,0,0)',  # Transparent legend background
            bordercolor='#7FDBFF',  # Baby blue color text
        )
    )
    return graph

# Slider tab 1 callback
@app.callback(
    Output('heatmap-graph', 'figure'),
    Input('day-slider', 'value')
)

def update_graph(day_index):
    day = day_order[day_index]
    return update_heatmap(day)

def update_heatmap(day):
    filtered_df = df[df['day_of_week'] == day]
    pizza_type_counts = filtered_df['pizza_flavor'].value_counts()
    popular_pizza_types = pizza_type_counts.nlargest(15).index.tolist() # for visibility. 
    filtered_df = filtered_df[filtered_df['pizza_flavor'].isin(popular_pizza_types)] # 32 pizza flavors were too much
    filtered_df['hour'] = pd.to_numeric(filtered_df['hour'])  
    filtered_df = filtered_df.sort_values('hour')  
    filtered_df['quantity'] = filtered_df['quantity'] / 52 # divide by 52 weeks to get average per week, rather than total per year
    heatmap_fig = px.density_heatmap(filtered_df, x='hour', y='pizza_flavor', z='quantity', color_continuous_scale='RdYlGn')
    heatmap_fig.update_layout(xaxis={'type': 'category'})  

    return style_graph(heatmap_fig)


@app.callback(
    Output('employee-area-chart', 'figure'),
    [Input('day-slider', 'value')]
)
def update_employee_area_chart(day_index):
    day = day_order[day_index]
    return generate_employee_area_chart(day)

def generate_employee_area_chart(day):
    daily_data = df[df['day_of_week'] == day]

    # Group by hour and calculate sum of quantity, 
    # then apply a function that determines the number of employees needed
    # based on the sum of quantity
    hourly_sum = daily_data.groupby('hour')['quantity'].sum()

    # 4 employees if more than (1040 in a year) 20 pizzas sold in an hour
    # average price of pizza is $ 20. Suppose margin is 50% = $10. 
    # profit is 20 * 10 = 200 an hour. Wage for 4 employees is 60 an hour. 
    # wage over proft ratio = 0.30

    # 3 employees if more than (780 in a year) 15 pizzas sold in an hour.
    # average price of pizza is $ 20. Suppose margin is 50% = $10. 
    # profit is 15 * 10 = 150 an hour. Wage for 3 employees is 45 an hour. 
    # wage over proft ratio = 0.30

    # 2 Employees if more than (520 in a year) 10 pizzas sold in an hour 
    # average price of pizza is $ 20. Suppose margin is 50% = $10.
    # profit is 10 * 10 = 100 an hour. Wage for 2 employees is 30 an hour.
    # wage over proft ratio = 0.30

    # 1 employee if more than (195 in a year) 3.75 pizzas sold in an hour
    # average price of pizza is $ 20. Suppose margin is 50% = $10.
    # profit is 3.75 * 10 = 37.5 an hour. Wage for 1 employee is 15 an hour.
    # wage over proft ratio = 0.4

    # 0 employees if less than (195 in a year) 3.75 pizzas sold in an hour (don't need to be open, price of wage > profit)
    hourly_employee_count = hourly_sum.apply(lambda x: 4 if x > 1040 else 3 if x > 780 else 2 if x > 520 else 1 if x > 195 else 0)

    # Calculate default_employee_count dynamically
    default_employee_count = hourly_sum.index.to_series().apply(lambda x: 3 if 10 < x < 20 else 2)

    # Create area chart
    area_chart_fig = go.Figure()
    area_chart_fig.add_trace(go.Scatter(
        x=hourly_employee_count.index,
        y=hourly_employee_count,
        fill='tozeroy',
        mode='none',  # Remove line markers
        name='Optimized Employee Count'
    ))

    # Add a dynamic line for the calculated default employee count
    area_chart_fig.add_trace(go.Scatter(
        x=default_employee_count.index,
        y=default_employee_count,
        mode='lines',
        name='Dynamic Default Employee Count',
        line=dict(color='red', dash='dash')
    ))

    # Update layout
    area_chart_fig.update_layout(
        title=f'Employee Count by Hour for {day}',
        margin=dict(l=140, r=40, t=40, b=40),
        xaxis_title='Hour',
        yaxis_title='Employee Count'
    )

    return style_graph(area_chart_fig)



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

def update_revenue_cost_rainfall_graph():
    # Assumes df and rain are pre-loaded DataFrames with relevant data
    rainfall_data = rain.groupby('month').sum()
    results = df.groupby('month')['price'].sum()
    months = list(range(1, 13))
    days_in_month = [calendar.monthrange(2015, month)[1] for month in months]
    adjusted_quantity = results / days_in_month 
    operating_costs = (adjusted_quantity * .4) + 500 # Adjust based on realistic business costs

    # Dynamic cost multiplier inversely proportional to rainfall
    base_cost_multiplier = 250
    max_rainfall = rainfall_data['rainfall'].max()
    normalized_rainfall = rainfall_data['rainfall'] / max_rainfall
    dynamic_cost_multiplier = 1 - normalized_rainfall  # Inverse relationship

    # Calculate optimized operating costs purely based on inverse rainfall relationship
    # Here, we adjust the base cost multiplier inversely with the normalized rainfall
    min_operating_cost = 1200  # Adjust based on realistic business costs
    optimized_operating_costs = (base_cost_multiplier * dynamic_cost_multiplier) + min_operating_cost

    # Ensure operating costs do not fall below the minimum threshold

    optimized_operating_costs = np.maximum(optimized_operating_costs, min_operating_cost)

    # Adding variability
    offset_percentage = 0.1
    variable_offset = optimized_operating_costs * offset_percentage
    np.random.seed(1)
    random_offsets = np.random.uniform(-1, 1, size=optimized_operating_costs.shape) * variable_offset
    optimized_operating_costs += random_offsets
    amount_spent1 = (operating_costs.sum()) * (365/12)
    amount_spent2 = (optimized_operating_costs.sum()) * (365/12)
    difference_in_op_cost = amount_spent1 - amount_spent2

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Traces
    fig.add_trace(go.Scatter(
        x=rainfall_data.index,
        y=rainfall_data['rainfall'],  # Actual Rainfall
        name='Rainfall',
        mode='lines+markers',
        marker=dict(color='blue')
    ), secondary_y=False)

    fig.add_trace(go.Scatter(
        x=list(range(1, 13)),
        y=operating_costs,
        name='Est. Daily Operating Costs(Based on revenue)',
        mode='lines',
        line=dict(color='red')
    ), secondary_y=True)

    fig.add_trace(go.Scatter(
        x=rainfall_data.index,
        y=optimized_operating_costs,
        name='Optimized Operating Costs (Weather Adjusted)',
        mode='lines',
        line=dict(color='green', dash='dot')
    ), secondary_y=True)

    # Layout updates
    fig.update_layout(
        title='Est. Operating Cost vs. Rainfall Adjusted Operating Costs',
        xaxis_title='Month',
        xaxis=dict(tickvals=list(range(1, 13)), ticktext=[calendar.month_name[i] for i in range(1, 13)]),
    )
 

    fig.update_yaxes(title_text="Rainfall (inches)", secondary_y=False)
    fig.update_yaxes(title_text="Operating Cost ($)", secondary_y=True)

    return style_graph(fig)


# Slider tab 3 callback
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
