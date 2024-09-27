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


ingredients_dummies = df['ingredients'].str.get_dummies(',')

# Add the new columns to the original DataFrame
df = pd.concat([df, ingredients_dummies], axis=1)
df = df.drop('ingredients', axis=1) # Drop the OG 'ingredients' column

hourly_sum_quantity = df.groupby(['day_of_week', 'hour'])['quantity'].sum()
hourly_df = hourly_sum_quantity.reset_index(name='Total Orders sold at this hour of this day')

weekday_employee_count = {
    10: 0, 11: 4, 12: 6, 13: 6, 14: 6, 15: 3, 16: 3, 17: 4, 18: 3, 19: 2, 20: 2, 21: 1, 22: 1, 23: 0
}

weekend_employee_count = {
    10: 0, 11: 3, 12: 3, 13: 4, 14: 4, 15: 3, 16: 3, 17: 4, 18: 4, 19: 3, 20: 3, 21: 2, 22: 1, 23: 0
}
# set the default employee count to 6 between 10am and 8pm, and 4 otherwise
# This is a very simple model, but it's a good starting point 
# used to find differences in employee count before and after changes



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
    'borderRadius': '25px',  # Rounded corners for selected tab
    'border-bottom': '2px solid #1975FA',  
    'border-top': '2px solid #1975FA',  
    'border-left': '2px solid #1975FA',  
    'border-right': '2px solid #1975FA'  
}

app.layout = html.Div(style={
    'backgroundColor': '#303030',  # Dark background always\
    'code': '{background-color: #7FDBFF; color: #7FDBFF;}',  # Code block color
    'color': '#FFFFFF',  # White text always
    'fontFamily': '"Roboto", sans-serif',  # custom font
    'margin': '-30px',  
    'minHeight': '90vh',  # Full view height
    'padding': '90px'  # Padding everywhere
}, children=[
    html.H1("Python for Business Analytics - Jean Batista (B.A)", style={'color': '#FFFFFF','textAlign': 'center','fontSize':'30px','marginBottom': '20px'}), # center text color white 
    dcc.Tabs(id="tabs", value='tab-0', children=[
        dcc.Tab(label='Introduction', value='tab-0', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Peak Hours and Operating costs', value='tab-1', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='The weather affects demand', value='tab-2', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Pie Sizes', value='tab-3', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Pizza toppings popularity', value='tab-4', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Conclusion', value='tab-5', style=tab_style, selected_style=tab_selected_style),
    ], style=tabs_styles),
    html.Div(id='content')
])

# Define the callback to update the content based on the selected tab
@app.callback(
    Output('content', 'children'),
    Input('tabs', 'value')
)

def render_content(tab):
    if tab == 'tab-0':
        return html.Div([
            html.H2('A restaurant owner states: “ I am looking to open a pizza restaurant, what suggestions do you have for success?" ', style={'color': '#FFFFFF','marginTop': '135px','fontSize': '30px','textAlign': 'center'}),  # Title

            html.P('My task here is to prepare and perform analysis on sales data to create a report detailing the opportunities for this client. Including charts and graphs that support my proposal. This project therefore uses SQL, Python, and some business intelligence tools (PyPlot & Dash) to present a suitable, polished report/presentation.', 
                   style={'color': '#7FDBFF', 'fontSize': '25px', 'marginBottom': '25px', 'marginTop': '60px', 'marginRight': '75px', 'marginLeft': '75px'}),
    
            html.P([
                'After completing a comprehensive analysis, I assisted this restaurant increase revenue and cut costs by about ',
                html.Span('$258,941.', style={'fontWeight': 'bold', 'color': '#5ae959'})
            ], style={'color': '#7FDBFF', 'fontSize': '25px', 'marginBottom': '25px', 'marginRight': '75px', 'marginLeft': '75px'}),
            
            html.P('Clicking on the tabs above will show the results of my analysis, including creating of graphs and charts.',
                   style={'color': '#7FDBFF', 'fontSize': '25px', 'marginBottom': '25px', 'marginRight': '75px', 'marginLeft': '75px'}),
        ])
    elif tab == 'tab-1':
        return html.Div([
            html.H2('The heatmap below shows concentration of orders from Open at 9 AM to Closing time at 11PM. Pay attention to their peak hours!', style={'color': '#FFFFFF','fontSize': '22px', 'marginTop': '64px','marginBottom': '35px', 'textAlign': 'center'}),  # Title
            
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
                html.Div(
                'Peak hours are usually at noon during weekdays. But on weekends, there is business at any given hour! The graph below shows the number of employees needed to meet the demand at each hour of the day. The red line represents amount of employees before, while the blue shade represents the amount of employees after proposed changes.',
                style={
                    'fontSize': '22px',  
                    'marginBottom': '70px',  
                    'textAlign': 'center',  
                    'color': '#7FDBFF',
                }
            ),
                html.Div([
                    html.H2('Employee Count Optimization', style={'color': '#FFFFFF','fontSize': '24px', 'marginTop': '70px', 'marginBottom': '50px', 'textAlign': 'center'}),]),
                dcc.Graph(id='employee-area-chart')  # New Graph for Employee Count
            ]),
            html.Div([
            html.H2('Cutting Costs:', style={'color': '#FFFFFF','fontSize': '30px'}),
            html.Div([
                html.P([
                'After reducing staff hours, the restaurant owner can save approximately ',
                html.Span('$82,680 annually', style={'fontWeight': 'bold', 'color': '#5ae959'}), 
                '( Based on assumed wage of $15/hr, and reduction of 106 hours per week on average).'
            ], style={'color': '#7FDBFF', 'fontSize': '25px', 'marginBottom': '25px', 'marginRight': '75px', 'marginLeft': '75px'}),
        ])
        ])
        ])
        
    elif tab == 'tab-2':
        return html.Div([ #plot for rainfall and sales, shows correlation between the two
            html.H2('Adverse relationships between weather and sales.', style={'color': '#FFFFFF','fontSize': '24px', 'marginTop': '70px'}),  # Title
            html.Div('Sales Data & Forecasts obtained Rain Data',
                style={
                    'fontSize': '18px',  
                    'marginBottom': '20px',  
                    'marginTop': '5px'  
                }
            ),
            dcc.Graph(
                id='subplot-graph',
                figure=update_subplot_graph()
            ),
            html.P('The rainfall has an impact on sales, likely due to consumer behavior. The business can use weather forecasts to know before-hand if their sales are to be affected that month, and can save money by planning ahead. I was able to change operating costs so that the business can manage factors like ordering & prepping ingredients, overstaffing, etc. The $ difference is estimated using a formula that standardizes operating costs based on orders made each month in relation to rain that month.', style={'fontSize': '20px', 'color': '#7FDBFF','marginBottom': '45px', 'marginTop': '35px', 'textAlign': 'center'}),
            html.H2('Average Operating Cost', style={'color': '#FFFFFF','fontSize': '24px'}),
            html.Div(
                'The restaurant can reduce operating costs by adjusting based on expected weather conditions.',
                style={
                    'fontSize': '18px',  
                    'marginBottom': '20px',  
                    'marginTop': '5px'  
                }
            ),
            dcc.Graph(
                id='cost-rainfall-graph',
                figure=update_revenue_cost_rainfall_graph()
            ),
            html.Div([
            html.H2('Proposed Changes:', style={'color': '#FFFFFF','fontSize': '24px'}),
            html.Div([
                html.P([ # calls back to formula used to estimate the difference in operating costs
                'After estimating the difference in operating costs, using the weather based formula, I assisted this restaurant cut costs by about ',
                html.Span('$30,780 anually', style={'fontWeight': 'bold', 'color': '#5ae959'}), 
                ' (6% reduction).'
            ], style={'color': '#7FDBFF', 'fontSize': '25px', 'marginBottom': '25px', 'marginRight': '75px', 'marginLeft': '75px'}),
        ])
        ])
        ])

    elif tab == 'tab-3':
        return html.Div([ # Pie chart and the greek pizza pie chart- shows the size distribution of sales, and advocation for XL and XXL sizes
        html.Div([
            dcc.Graph(
                id='pie-chart',
                figure=update_pie_chart(),
                style={'width': '48%', 'display': 'inline-block', 'marginTop': '70px'}
            ),
            dcc.Graph(
                id='the-greek',
                figure=the_greek(),
                style={'width': '48%', 'display': 'inline-block','marginTop': '70px'}
            )
        ], style={'display': 'flex', 'justifyContent': 'space-between'}),
        html.Div([ # Text below the pie chart excplaing the analysis ( greeek pizza)
            html.P('Overview of Findings:', style={'fontSize': '24px', 'color': '#FFFFFF', 'fontWeight': 'bold','marginTop': '30px' ,'marginBottom': '20px', 'textAlign': 'center'}),
            html.P('Objective: The analysis aimed to quantify potential revenue gains by offering XL and XXL pizza sizes for all menu flavors, based on the current sales distribution of "The Greek" pizza, which is the only pizza flavor offered in these larger sizes.', style={'fontSize': '20px', 'color': '#7FDBFF', 'marginBottom': '10px'}),
            html.P('Standardized Revenue Comparison:', style={'fontSize': '24px', 'color': '#FFFFFF', 'fontWeight': 'bold', 'marginTop': '30px','marginBottom': '10px', 'textAlign': 'center'}),
            html.P('To standardize the comparison, we assumed 100 pizzas are ordered in each scenario.', style={'fontSize': '20px', 'color': '#7FDBFF', 'marginBottom': '10px'}),
            html.P('Current Revenue for All Other Flavors (small, medium, large): Based on the size distribution of sales across all other pizzas, the estimated revenue per 100 pizzas is $1,463.26.', style={'fontSize': '20px', 'color': '#7FDBFF', 'marginBottom': '10px'}),
            html.P('Current Revenue for "The Greek" (small, medium, large, XL, XXL): With XL and XXL sizes included, the estimated revenue per 100 pizzas is $1,728.73.', style={'fontSize': '20px', 'color': '#7FDBFF', 'marginBottom': '10px'}),
            html.P('Opportunity Gains:', style={'fontSize': '24px', 'color': '#FFFFFF', 'fontWeight': 'bold', 'marginTop': '30px','marginBottom': '10px', 'textAlign': 'center'}),
            html.P('The difference in revenue per 100 pizzas between "The Greek" and all other flavors is $265.47, which represents an 18.14% increase in revenue when XL and XXL sizes are available.', style={'fontSize': '20px', 'color': '#7FDBFF', 'marginBottom': '10px'}),
            html.P([
                'Extrapolating this ',
                 html.Span('18.14% ', style={'fontWeight': 'bold', 'color': '#5ae959','fontSize': '22px'}),  'increase to the restaurant\'s total annual sales of $801,994, the estimated total revenue would grow to $947,475, resulting in an additional ',
                html.Span('$145,481 annually.', style={'fontWeight': 'bold', 'color': '#5ae959', 'fontSize': '22px'}), 
            ], style={'fontSize': '20px', 'color': '#7FDBFF', 'marginBottom': '10px'}),
            html.P('Customer Behavior Insights:', style={'fontSize': '24px', 'color': '#FFFFFF', 'fontWeight': 'bold', 'marginTop': '30px','marginBottom': '10px', 'textAlign': 'center'}),
            html.P('The XL size of "The Greek" is highly popular, accounting for 38.9% of its total sales. This indicates a strong customer preference for larger sizes when they are available.', style={'fontSize': '20px', 'color': '#7FDBFF', 'marginBottom': '10px'}),
            html.P('Applying this behavior to other popular pizza flavors could similarly boost the average order value, particularly for group or family orders.', style={'fontSize': '20px', 'color': '#7FDBFF', 'marginBottom': '10px'}),
        ])
    ])
    elif tab == 'tab-4': 
        return html.Div([
            html.H2('Popularity per Topping Group', style={'color': '#FFFFFF','fontSize': '24px', 'marginTop': '40px', 'marginBottom': '25px'}),  
            html.Label("Select a month:", style={'font-weight': 'bold', 'display': 'block', 'margin-bottom': '5px'}),
            dcc.Slider( # Slider for selecting the month, for popularity per topping group
                id='month-slider',
                min=df['month'].min(),
                max=df['month'].max(),
                value=df['month'].min(),
                marks={int(i): {'label': calendar.month_name[i], 'style': {'transform': 'rotate(-45deg)', 'white-space': 'nowrap'}} # labeling months on slider
       for i in df['month'].unique()},
                step=None,
            ),
            html.Div(
                id='selected-pizza-stats',
                # This will display the selected pizza statistics, add some space below this div
                style={'margin-bottom': '20px'}  
            ),
            dcc.Graph(
                id='scatterplot',
                # Call the function with the default slider value
                figure=update_scatterplot(df['month'].min()),
                style={'margin-top': '20px'}  
            )
        ])
    elif tab == 'tab-5':
        return html.Div([
            html.H2('Overview ', style={'color': '#FFFFFF','marginTop': '80px','fontSize': '30px','textAlign': 'center'}),  # Title

            html.P([
                'Analysis of peak hours allowed me to establish a system of allocating staff hours in the most effective way. Saving approximately ', # Paragraph 1 (hours)
                html.Span('$79,560 annually.', style={'fontWeight': 'bold', 'color': '#5ae959'})
            ], style={'color': '#7FDBFF', 'fontSize': '25px', 'marginBottom': '25px', 'marginRight': '75px', 'marginLeft': '75px'}),
            
            html.P([
                'Using a weather forecasts to predict how busy business is, gives the chance to allocate funds most effectively, the model suggests that this change cuts costs by about ', # Paragraph 2 (weather)
                html.Span('$30,780 anually.', style={'fontWeight': 'bold', 'color': '#5ae959'})
            ], style={'color': '#7FDBFF', 'fontSize': '25px', 'marginBottom': '25px', 'marginRight': '75px', 'marginLeft': '75px'}),

            html.P([
                'The potential revenue gains by offering XL and XXL pizza sizes for all menu flavors is estimated to be ', # Paragraph 3 (pizza sizes)
                html.Span('$145,481 annually', style={'fontWeight': 'bold', 'color': '#5ae959'}),
                ', based on the current sales distribution of these larger sizes, indicating a boosts in order value.'
            ], style={'color': '#7FDBFF', 'fontSize': '25px', 'marginBottom': '25px', 'marginRight': '75px', 'marginLeft': '75px'}),

            html.P([
                'The total potential gains estimated to be ', # Paragraph 4 (total)
                html.Span('$258,941 annually.', style={'fontWeight': 'bold', 'color': '#5ae959'})
            ], style={'color': '#7FDBFF', 'fontSize': '25px', 'marginBottom': '25px', 'marginRight': '75px', 'marginLeft': '75px'}),

            html.P('For more detailed information and to view the source code, please visit the GitHub repository:'), # Paragraph 5 (GitHub)
            dcc.Link('Visit GitHub Repository', href='https://github.com/CCNY-Analytics-and-Quant/DA-Business-Analytics-2023', target='_blank', style={
             'color': '#7FDBFF',
                'fontSize': '20px',
                'display': 'block',
                'textAlign': 'center',
                'marginTop': '30px',
            }),
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
    heatmap_fig = px.density_heatmap(filtered_df, x='hour', y='pizza_flavor', z='quantity', color_continuous_scale='ice')
    heatmap_fig.update_layout(xaxis={'type': 'category'})
    heatmap_fig.update_coloraxes(colorbar_title="Average sales")  # Update color bar title

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

    if day in ['Saturday', 'Sunday']:
        employee_count_structure = weekend_employee_count
    else:
        employee_count_structure = weekday_employee_count
    
    hourly_employee_count = hourly_sum.index.to_series().map(employee_count_structure).fillna(0)
    # Calculate default_employee_count dynamically
    default_employee_count = hourly_sum.index.to_series().apply(lambda x: 5 if 10 < x < 20 else 3)

    # create the line for employee count before changes made 
    area_chart_fig = go.Figure()
    area_chart_fig.add_trace(go.Scatter(
        x=default_employee_count.index,
        y=default_employee_count,
        mode='lines',
        name='Employee Count Before',
        line=dict(color='red')
    ))
    # Create the after line for employee count after changes made
    area_chart_fig.add_trace(go.Scatter(
        x=hourly_employee_count.index, #calls back to the function that determines the number of employees needed per demand
        y=hourly_employee_count,
        mode='lines',
        line=dict(color='green'),
        name='Employee Count After'
    ))

    # Update layout
    area_chart_fig.update_layout(
        title=f'Save Costs on staffing! Proposed changes on Employee Count by Hour for {day} based on live data on sales!',
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
    fig.add_trace(go.Scatter(x=months, y=adjusted_quantity, name='Sales', line=dict(color='green')), secondary_y=False)
    fig.add_trace(go.Scatter(x=months, y=rainfall['rainfall'], name='Rainfall', line=dict(color='#3076ff')), secondary_y=True)
    fig.update_layout(
        xaxis=dict(title='Month', dtick=1),
        yaxis=dict(
            title='Sales per day',
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
        legend=dict(x=0, y=1.2, orientation='h'),
        width=1500,
        height=500
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
        line=dict(color='#3076ff',dash='dash')
    ), secondary_y=False)

    fig.add_trace(go.Scatter(
        x=list(range(1, 13)),
        y=operating_costs,
        name='Operarting Costs Before (Estimate)',
        mode='lines',
        line=dict(color='red')
    ), secondary_y=True)

    fig.add_trace(go.Scatter(
        x=rainfall_data.index,
        y=optimized_operating_costs,
        name='Operating Costs After (Estimate)',
        mode='lines',
        line=dict(color='green')
    ), secondary_y=True)

    # Layout updates
    fig.update_layout(
        xaxis_title='Month',
        xaxis=dict(tickvals=list(range(1, 13)), ticktext=[calendar.month_name[i] for i in range(1, 13)]),
    )
 

    fig.update_yaxes(title_text="Rainfall (Inches)", secondary_y=True)
    fig.update_yaxes(title_text="Operating Cost ($)", secondary_y=False),
    width=1000,
    height=500

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
        labels={'quantity': 'Sales'},
        size='quantity',  # Optional: Use the quantity as the size of the scatter plot markers
        hover_name='pizza_flavor')  # Optional: Show the pizza flavor name on hover

    # Update layout
    scatterplot_fig.update_layout(xaxis={'categoryorder': 'total descending'})

    return style_graph(scatterplot_fig)


# I have the pie chart to evaluate if XL and XXL are viable options
def update_pie_chart():
    sizes = df.groupby('size')['quantity'].sum().reset_index()
    size_order = ['S', 'M', 'L', 'XL', 'XXL']
    sizes['size'] = sizes['size'].astype('category')
    sizes['size'] = sizes['size'].cat.set_categories(size_order)
    sizes.sort_values("size", inplace=True)

    pie_color_pallete = ['rgb(20,169,233)', 'rgb(146,20,233)','rgb(20,233,22)','rgb(233,35,20)','rgb(221, 233, 20)']
    pie_chart_fig = go.Figure(data=go.Pie(labels=sizes['size'], values=sizes['quantity'], marker=dict(colors=pie_color_pallete), hole=0.9, sort=False))
    pie_chart_fig.update_layout(title='Sales by Sizes:',showlegend=True)
    return style_graph(pie_chart_fig)


def the_greek():
    greek_df = df[df['pizza_flavor'] == 'the_greek']
    greek_group = greek_df.groupby('size')['quantity'].sum().reset_index()
    size_order = ['S', 'M', 'L', 'XL', 'XXL']
    greek_group['size'] = greek_group['size'].astype('category')
    greek_group['size'] = greek_group['size'].cat.set_categories(size_order)
    greek_group.sort_values("size", inplace=True)
    pie_color_pallete = ['rgb(20,169,233)', 'rgb(146,20,233)','rgb(20,233,22)','rgb(233,35,20)','rgb(221, 233, 20)']

    greek_chart_fig = go.Figure(data=go.Pie(labels=greek_group['size'], values=greek_group['quantity'],marker=dict(colors=pie_color_pallete), sort= False, hole=0.9))
    greek_chart_fig.update_layout(title='The Greek is the only pizza available in XL & XXL, "The Greek" Sales by Sizes:',
                                showlegend=True)


    return(style_graph(greek_chart_fig))

if __name__ == '__main__':
    app.run_server()
