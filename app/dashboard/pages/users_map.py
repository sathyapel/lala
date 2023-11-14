from dash import html, callback, Output, Input
import dash_mantine_components as dmc
from dash import dcc
import pandas as pd


class UsersOnMap:

    def __init__(self):
        self.parent_kids_df = pd.read_csv('parent_kids.csv')

        self.map = None
        self.mapContainer = html.Div(
            className="", children=[
                dmc.Header(id="content_header", className="flex-row ", children=[
                    dmc.Stack(children=[
                        dmc.Text(children="Users on Map",
                                 className="font-sans text-left lg:text-2xl",p=12),
                        dmc.Divider(
                            label="Overview", className="font-sans", labelPosition="right",p=12)]
                    )

                ], height=120),
                



                html.Iframe(src="http://localhost:8000/analytics/mapsonlala/allusers",
                            style={"height": "300px", "width": "100%", "background": "#DDDDDD"})

            ])

    def get(self):
        # self.setCallbacks()
        return self.mapContainer
