from dash import html,callback, Output, Input
import dash_mantine_components as dmc
from dash_iconify import DashIconify

class HeaderComponent():
    def __init__(self,height=50,withBorder=True) :    
         self.header = dmc.Header(
            height=height,
            withBorder=withBorder,
            bg="#3182CE",
            m=0,
            
            className="flex items-center justify-between gap-0",   
            children=[
                          
                            html.Div(className="w-full",
                            children=[ dmc.Text(
                                
                                "Lala Analytics",
                                className= "font-sans text-yellow-100 text-center lg:text-xl",
                                
                   
                                )]),
                                
                            html.Div(className="w-min mr-1 lg:mr-2 overflow-hidden",
                                children=[
                                dmc.Switch(
                                id="switch-theme",
                                offLabel=DashIconify(icon="radix-icons:moon", width=20),
                                onLabel=DashIconify(icon="radix-icons:sun", width=20),
                                size="sm",
                                checked="False")
                                 ],)

                                

                            
                        ]
                    )
                    
                
         
               
                

        
    
    def setCallbacks(self):
        @callback(
        Output('app-theme', 'theme'),
        Input('app-theme', 'theme'),
        Input("switch-theme", "checked"),
        prevent_intial_call=True)
        def switch_theme(theme, checked):
            if not checked:
                theme.update({'colorScheme': 'dark'})
            else:
                theme.update({'colorScheme': 'white'})
            return theme
        
    def get(self)->dmc.Header:
        print("typehead",type(self.header))
        self.setCallbacks()
        return self.header       
    



         
    


