import dash_mantine_components as dmc
from dash import html
from .header import HeaderComponent
from typing import Optional
from dash_iconify import DashIconify
from typing import List,Any
from app.dashboard.pages.users_map import UsersOnMap
import pandas as pd


class ContentComponent():
    def __init__(self, content_header: str,nav_type:str,content_page):
        self.contentComponent = html.Div(
            id=f"content_component_{content_header}",
            children=[
               
                
                content_page



            ]
        )

    def get(self):
        return self.contentComponent
