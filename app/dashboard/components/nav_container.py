
import dash_mantine_components as dmc
from dash import html, callback, Output, Input, ctx
from .header import HeaderComponent
from typing import Optional
from dash_iconify import DashIconify
from .content import ContentComponent
from typing import List
from app.dashboard.pages.users_map import UsersOnMap
from app.dashboard.pages.dashboard import DashBoard


def get_icon(icon):
    return DashIconify(icon=icon, height=16)


class NavContainer:
    def __init__(self, tailWindStyle: Optional[str] = None, navLinks: dict = {"Dashboard": "ic:round-dashboard-customize",
                                                                              "Trend Analysis": "ic:twotone-timeline",
                                                                              "Users on Map": "ic:baseline-map"

                                                                              }):
        self.navLinks = navLinks
        self.navController = html.Div(
            style={
                "background": "rgb(72,93,119)", "background": "linear-gradient(180deg, rgba(72,93,119,1) 13%, rgba(48,133,233,1) 82%);"},
            id="nav_controller",
            className=tailWindStyle if tailWindStyle != None else "",
            children=[
                html.Div(
                    className="inset-0 flex-row",
                    children=[
                        HeaderComponent(50, withBorder=False).get(),
                        dmc.Divider(id="header_divider", variant="solid", style={
                                    "height": 15}, color="#4E6980"),
                        html.Div(id="nav_link_div",
                                 children=[
                                     html.Div(id="nav_links",

                                              children=[
                                                  bulid_buttons(self.navLinks)



                                              ]

                                              )

                                 ])

                    ]
                )

            ]
        )

    def setCallbacks(self):
        @callback(
            Output("content_div_sub", "children"),
            [Input("nav_btn_container_{}".format(link_name), "n_clicks") for link_name in self.navLinks],
            prevent_initial_call=True)
        def navigate_to(*vals):
            recent_btn_id = f"nav_btn_container_{Set(self.navLinks.keys()).first_or_null()}"
            recent_nav_key = Set(self.navLinks.keys()).first_or_null()
            navigate_btns = [val for val in vals]
            for nav_id in self.navLinks.keys():
                if f"nav_btn_container_{nav_id}" == ctx.triggered_id:
                    recent_btn_id = f"nav_btn_container_{nav_id}"
                    recent_nav_key = nav_id
                    break
                

            if nav_id == "Users on Map" :
                return ContentComponent(recent_btn_id,recent_nav_key,UsersOnMap().get()).get()
            elif nav_id == "Trend Analysis":
                return ContentComponent(recent_btn_id,recent_nav_key,None).get()
            else:
                return ContentComponent(recent_btn_id,recent_nav_key,DashBoard().get()).get()
             
            

    def get(self) -> html.Div:
        self.setCallbacks()
        return self.navController


def bulid_buttons(nav_buttons: dict):
    """Build buttons for navigation

    Add dashIconfy object strings for icons

    `nav_buttons`: navigation labels and icon links if no icon place None """
    buttons = []
    for link_name, dmc_icon_link in nav_buttons.items():
        buttons.append(
            html.Div(
                n_clicks=0,
                id=f"nav_btn_container_{link_name}",
                children=dmc.Group(
                    className="flex flex-row py-1 hover:bg-blue-800 ",
                    children=[
                        DashIconify(icon=dmc_icon_link,
                                    color="white", className="ml-3"),
                        html.H6(id=f"link_{link_name}",
                                children=link_name, className="font-sans text-white text-start lg:text-md")

                    ]


                )
            )


        )

    stackOfButtons = dmc.Stack(children=[button for button in buttons])
    return stackOfButtons


class Set(set):
    '''
    it is user-defined class inherited from `set` use only when it is needed
    '''
    def to_list(self):
        return list(self)

    def first_or_null(self):
        ''' gets first item of `set` or  `None` instead '''
        if all([self != None, len(self) > 0]):
           
            return self.to_list()[0]
        else:
            return None
