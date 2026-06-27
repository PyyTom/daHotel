import flet
class UI:
    def __init__(self,page:flet.Page):
        self.page=page
    def alert(self,title,actions):
        return flet.AlertDialog(title=flet.Text(title),actions=actions)
    def row(self,controls,width,height,alignment,scroll):
        return flet.Row(controls=controls,width=width,height=height,alignment=alignment,scroll=scroll)
    def column(self,controls,width,height,scroll):
        return flet.Column(controls=controls,width=width,height=height,scroll=scroll)
    def divider(self):
        return flet.Divider()
    def v_divider(self):
        return flet.VerticalDivider()
    def switch(self,on_change):
        return flet.Switch(on_change=on_change)
    def text(self,value,size,color):
        return flet.Text(value=value,size=size,color=color)
    def tf(self,label,value,width,type):
        return flet.TextField(label=label,value=value,width=width,keyboard_type=type)
    def button(self,text,color,on_click):
        return flet.ElevatedButton(content=text,color=color,on_click=on_click)
    def iconbutton(self,icon,size,color,on_click):
        icon_v=getattr(flet.Icons,icon)
        return flet.IconButton(icon=icon_v,icon_size=size,icon_color=color,on_click=on_click)
    def dd(self,label,value,options,color):
        return flet.Dropdown(label=label,value=value,options=[flet.DropdownOption(text=option) for option in options],color=color,width=200)
    