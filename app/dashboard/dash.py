from dash import Dash, html, dash_table,dcc,callback, Output, Input
import pandas as pd
import plotly.express as px
import os
import numpy as np

def moveToSavedModel():
    if not(os.getcwd().__contains__("saved_model")):
          cur_dir = os.getcwd()
          app_dir_path = os.path.join(cur_dir,"app")
          os.chdir(app_dir_path)
          init_data_path=os.path.join(os.getcwd(),"saved_model")
          os.chdir(init_data_path)
# Incorporate data

moveToSavedModel()

df = pd.read_csv('stories.csv')
story_counts = df["category"].value_counts().reset_index().iloc[:11]

# Initialize the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
dashApp = Dash(__name__,requests_pathname_prefix="/analytics/",external_stylesheets=external_stylesheets)

# App layout
dashApp.layout = html.Div(className="row",children=[
    
    html.Div(className="row",children='LalaAnalytics',style={"textAlign":"center",'color':'red','fontSize':30}),
    html.Div(className="row",children=[
         html.Div(className="six columns",children=[
           dash_table.DataTable(data=df.to_dict('records'), page_size=10,dropdown='category')
    ])
    ]),
    dcc.Graph(id="stories_graph1",figure=px.bar(story_counts,x='category',y='count',title='Top 10 Categories Published')),
    html.Hr(),
    html.H4(className="row", children="Top stories By categories"),
    html.Div(className="row",children=[
        html.Div(className="six columns",children=[ dcc.RadioItems(options=
            [str(x) for x in df["language"].unique()],value='5',id='lang-option-radio')]),
        html.Div(className="six columns",children=[
             dcc.Graph(id='lang-option-output',figure={})
        ])    
    
    ])
            
])

@callback(
    Output(component_id='lang-option-output', component_property='figure'),
    Input(component_id='lang-option-radio', component_property='value')
)

def update_graph(col_chosen):
    print("choosen_option",type(col_chosen))
    lang=df['language'].astype(str)
    cat_df=df[lang==col_chosen]["category"].value_counts().reset_index().iloc[:11]
    fig = px.bar(cat_df,x='category',y='count',title='Top 10 Categories Published')
    return fig

# Run the app
if __name__ == '__main__':
    dashApp.run(debug=True)