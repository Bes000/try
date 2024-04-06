import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px



# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
site_names = spacex_df['Launch Site'].unique()
piedata = spacex_df.groupby('Launch Site')['class'].mean()
piedata = piedata*100
suc = pd.DataFrame([[26, 13, 10, 7],[7, 10, 4, 3]] ,columns= ['CCAFS LC-40', 'KSC LC-39A','VAFB SLC-4E','CCAFS SLC-40'],
                   index= ['suc', 'fail'])# Create a dash application
version =[]

for i in range(len(spacex_df['Booster Version'])):
    version.append(spacex_df['Booster Version'][i].split(' ')[1])
spacex_df['version'] = version   
    
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[ html.H1('SpaceX Launch Records Dashboard',
                                style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown', options= [
                                    {'label' : 'All Sites', 'value' : 'All'}]+
                                    [{'label' : i , 'value' : i} for i in site_names

                             
                                    
                                ],
                                value = 'All',
                                placeholder = 'select the site',
                                searchable = True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',min =0,
                                                max = 10000,step = 1000,
                                                marks ={0 : '0',
                                                        5000 : '5000'},
                                                        value = [0 , 10000]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id= 'success-pie-chart', component_property= 'figure'),
    Input(component_id= 'site-dropdown', component_property= 'value')
    
)
def get_pie_chart(site):
    if site =='All':
        fig = px.pie(piedata, values= (piedata),
                     names= site_names,
                     )
        return fig
    else:
        data = [(suc[site].iloc[1]), (suc[site].iloc[0]-suc[site].iloc[1])]
        fig = px.pie(data, values = data, names = ['success', 'fail'])
        return fig



# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id= 'success-payload-scatter-chart', component_property= 'figure'),
    [Input(component_id= 'site-dropdown', component_property= 'value'),
    Input(component_id = 'payload-slider', component_property = 'value')]
    
)

def get_scatter_plot(site, payload):
    if site == 'All':
        fig = px.scatter(x=spacex_df['Payload Mass (kg)'][(spacex_df['Payload Mass (kg)'] > payload[0]) & (spacex_df['Payload Mass (kg)'] < payload[1])],
                         y =spacex_df['class'][(spacex_df['Payload Mass (kg)'] > payload[0]) & (spacex_df['Payload Mass (kg)'] < payload[1])],
                           )
        fig.update_layout(xaxis_title="Payload Mass (kg)",yaxis_title="Class",
                          title = 'Payload vs. Launch Outcome')
       
                        
        return fig
    else:
        title = f'Payload vs. Launch Outcome for ({site})'
        fig1 = px.scatter(x = spacex_df['Payload Mass (kg)'][(spacex_df['Payload Mass (kg)'] > payload[0])&(spacex_df['Payload Mass (kg)'] < payload[1]) & (spacex_df['Launch Site'] == site)],
                                                             y = spacex_df['class'][(spacex_df['Payload Mass (kg)'] > payload[0])&(spacex_df['Payload Mass (kg)'] < payload[1]) & (spacex_df['Launch Site'] == site)],
                                                             )
        fig1.update_layout(
        xaxis_title="Payload Mass (kg)",
        yaxis_title="Class",
        title = title
        )

        return fig1

       


# Run the app
if __name__ == '__main__':
    app.run_server(debug = True)
