
import dash_mantine_components as dmc


class FooterComponent():
    def __init__(self,fixed_to_root:bool=True) :    
         self.footer = dmc.Footer(
            height=20,
            withBorder=True,
            fixed=fixed_to_root,
            children=[
                dmc.Center(
                   dmc.Text(
                    "©2022-2023",

                    className= "text-lime-300 text-sm",
                   
                ) 
                )
                ]
                
        ),

        
    
    def setCallbacks(self):
        pass
        
    def get(self)->dmc.Footer:
        self.setCallbacks()
        return self.footer[0]        
    



         
    


