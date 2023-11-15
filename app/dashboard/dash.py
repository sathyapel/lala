
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import os
import numpy as np
from app.core.config import settings
from flask_sqlalchemy import SQLAlchemy
from app.db.model import Base
from sqlalchemy import select
from app.db.model import LanguageModel
import dash_mantine_components as dmc
from app.dashboard.components.header import HeaderComponent
from app.dashboard.components.footer import FooterComponent
from app.dashboard.components.nav_container import NavContainer
from app.dashboard.components.content import ContentComponent
from dash_iconify import DashIconify
from flask import render_template_string
import folium
from folium import Choropleth, Circle, Marker
from folium.plugins import HeatMap, MarkerCluster


from app.dashboard.pages.dashboard import DashBoard
def moveToSavedModel():
    if not (os.getcwd().__contains__("saved_model")):
        cur_dir = settings.ROOT_PATH
        app_dir_path = os.path.join(cur_dir, "app")
        os.chdir(app_dir_path)
        init_data_path = os.path.join(os.getcwd(), "saved_model")
        os.chdir(init_data_path)
        print("currentPath::", os.getcwd())
# Incorporate data

moveToSavedModel()


df = pd.read_csv('stories.csv')
story_counts = df["category"].value_counts().reset_index().iloc[:11]

# Initialize the app
external_stylesheets = ["https://unpkg.com/tailwindcss@^1.0/dist/tailwind.min.css",
                        "https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;900&display=swap"]

dashApp = Dash(__name__, requests_pathname_prefix="/analytics/",
               external_stylesheets=external_stylesheets)

#db = SQLAlchemy(model_class=Base)
#dashApp.server.config["SQLALCHEMY_DATABASE_URI"] = settings.DATABASE_URL
#db.init_app(dashApp.server)


'''with dashApp.server.app_context():
    db.reflect()'''


'''@dashApp.server.route("/dba")
def dba():
    print(db.Model.metadata.tables.keys())
    language = LanguageModel(name="Malayalam", status=1,
                             lang_code="mal", deleted_at=None)
    db.session.add(language)
    db.session.commit()

    return "Hi" '''

@dashApp.server.route("/mapsonlala/allusers")
def getAllUsers():
    """Embed a map as an iframe on a page."""
    
    m = folium.Map()

   

    m = folium.Map(location=[41.9, -97.3], zoom_start=4)
    '''mc = MarkerCluster()
    for idx, row in pd.read_csv('parent_kids.csv').iterrows():
        if row['latitude'] != "unknown":
          if not math.isnan(float(row['latitude'])) and not math.isnan(float(row['longitude'])):
                mc.add_child(Marker([row['latitude'], row['longitude']], popup=row['name']))
    m.add_child(mc)  '''        
    iframe = m.get_root()._repr_html_()

    return render_template_string(
        """
            <!DOCTYPE html>
            <html>
                <body>
                    {{ iframe|safe }}
                </body>
            </html>
        """,
        iframe=iframe,
    )
# App layout


dashApp.layout = html.Div(
    dmc.MantineProvider(
    id="app-theme",
    theme={
        "colorScheme": "dark",
        "primaryColor": "indigo"

    },
    inherit=True,
    withGlobalStyles=True,
    withNormalizeCSS=True,
    children=[
        html.Div(
            children=[
                html.Div(
                    className="flex-row",
                    children=[
                        NavContainer(
                            tailWindStyle="bg-blue-600 lg:w-1/5 lg:h-screen lg:fixed lg:left-0").get(),
                        html.Div(
                            id="content_div",
                            className="lg:w-4/5 lg:absolute lg:right-0",
                            children=[
                                html.Div(
                                      id="content_div_sub",
                                      children=ContentComponent("default dash","Dashboard",DashBoard().get()).get()
                                ),
                                
                            ]
                        )
                    ]
                )
            ]),

    ]))


# Run the app
if __name__ == '__main__':
    dashApp.run(debug=True)
