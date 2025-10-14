import bpy
import os
from . import modules
PyBtnBox = modules

icon_in_blender = bpy.types.UILayout.bl_rna.functions["prop"].parameters["icon"].enum_items.keys()

AreaData = [['3D Viewport','VIEW3D'],
            ['Image Editor','IMAGE'],
            ['UV Editor','UV'],
            ['Compositor','NODE_COMPOSITING'],
            ['Texture Node Editor','NODE_TEXTURE'],
            ['Geometry Node Editor','GEOMETRY_NODES'],
            ['Shader Editor','SHADING_RENDERED'],
            ['Video Sequencer','SEQUENCE'],
            ['Dope Sheet','ACTION'],
            ['Graph Editor','GRAPH'],
            ['Drivers','DRIVER'],
            ['Nonlinear Animation','NLA'],
            ['Text Editor','TEXT'],
            #['Timeline','TIME']
            ]

# { MENU }
class MenuLayout:
    @staticmethod
    def draw_panel(self,context,Menu_ID):
        layout = self.layout
        pybtnbox_prop = context.scene.pybtnbox_prop
        folderName = pybtnbox_prop.get(Menu_ID,'')

        Menu = PyBtnBox.Menu.from_menu_name(folderName)
        if Menu.root_path == '': # if get wrong Root path
            box = layout.box()
            box.label(text = 'Not Found Root Folder',icon='ERROR')
            return 
        
        # Menu Picker
        row_menu = layout.row(align=True)
        menuIcon = Menu.icon if Menu.icon in icon_in_blender else 'NONE'
        row_menu.prop(pybtnbox_prop,Menu_ID,text='',icon=menuIcon)

        if Menu.json_path == '': # if get wrong Menu data
            layout.label(text = 'Not Found This Menu In Folder',icon='QUESTION')
            return 

        layout.separator(factor=2.0,type='LINE')
        

        layout_tree = [self.layout]
        menuData = Menu.json
        pyBtns = [btn for btn in menuData.keys() if btn != '__menuAttributes__']
        btnTreeLevel =0
        for pyBtn in pyBtns :
            btnData = menuData.get(pyBtn,None)
            if not btnData:
                continue
            btnLO = btnLayout(
                name   = pyBtn,
                is_ui =  btnData.get('is_ui',True),
                text   = btnData.get('text',''),
                pyPath = os.path.join(Menu.menu_path,f'{pyBtn}.py'),#pyBtnBox.Path.pyfile(folder,pyBtns[i]),
                icon   = btnData.get('icon','NONE'),
                type   = btnData.get('type',0),
                tip   = btnData.get('tip',''),
                )
            layout_tree,btnTreeLevel = btnLO.draw_panel(btnTreeLevel,layout_tree)


# { Normal Menu Button }
class btnLayout:
    def __init__(self,name,is_ui,text,pyPath,icon,type,tip):
        self.name = name
        self.is_ui = is_ui
        self.text = text
        self.pyPath = pyPath
        self.icon = icon
        self.type = type
        self.tip = tip
    # panel Root
    def draw_panel(self,btnTreeLevel,layout_tree):
        if not self.is_ui : # Button
            self.pn_exe_button(layout_tree,btnTreeLevel) 
            return layout_tree,btnTreeLevel
        #if self.type == 0: # Button
        #    self.pn_exe_button(layout_tree,btnTreeLevel) 
        #    return layout_tree,btnTreeLevel
        if self.type == 0: # label
            self.pn_exe_label(layout_tree,btnTreeLevel)# layout.panel(idname=self.name, default_closed=False)
            return layout_tree,btnTreeLevel
        if self.type == 1: # Panel
            layout_tree,btnTreeLevel = self.pn_exe_panel(layout_tree,btnTreeLevel)# layout.panel(idname=self.name, default_closed=False)
            return layout_tree,btnTreeLevel
        
        if self.type == 2: # End
            btn_panel,btnTreeLevel = self.pn_exe_end(layout_tree,btnTreeLevel) 
            return btn_panel,btnTreeLevel
        
    
    # panel type
    # Button Type
    def pn_exe_button(self,layout_tree,btnTreeLevel):
        layout = layout_tree[btnTreeLevel]
        if not layout:
            return
        row = layout.row(align = True)
        if self.icon != 'NONE':
            icon = self.icon if self.icon in icon_in_blender else 'ERROR'
            textBtn = row.operator("pybtnbox.button_description",text='',icon=icon,emboss=True)
            textBtn.btnName =self.name
            textBtn.text =self.tip
        row.operator("pybtnbox.button_execute" ,text= self.text).File = self.pyPath

        return 
    #0 Label Type
    def pn_exe_label(self,layout_tree,btnTreeLevel):
        layout = layout_tree[btnTreeLevel]
        if not layout:
            return layout_tree,btnTreeLevel
        
        row = layout.row()
        # icon
        label_icon = self.icon
        if not label_icon in icon_in_blender :
            label_icon ='NONE'
        if label_icon !='NONE':
            row.label( text=''  ,icon= label_icon )

        col = row.column(align=True)
        col.alignment='LEFT'
        Text_list = self.text.split(r'\n')
        for Txt in Text_list:
            col.label(text=Txt if Txt!='' else ' ' ,icon='NONE')
        col.alignment='RIGHT'

        return layout_tree,btnTreeLevel

    #1 Panel Type
    def pn_exe_panel(self,layout_tree,btnTreeLevel):
        layout = layout_tree[btnTreeLevel]
        if not layout :
            layout_tree.append(None)
            return layout_tree,btnTreeLevel+1
        btn_panel = layout.panel(idname=self.name, default_closed=False)
        if not self.icon in icon_in_blender:
            btn_panel[0].label(text=self.text)
        else :
            btn_panel[0].label(text=self.text,icon=self.icon)

        # Edit Area (is self open)
        edit_layout = btn_panel[1]
        if edit_layout:
            row = edit_layout.row(align=True)
            row.label(text='',icon="BLANK1")
            layout_tree.append(row.column())
        else:
            layout_tree.append(None)
        return layout_tree,btnTreeLevel+1

    #2 Return Type
    def pn_exe_end(self,layout_tree,btnTreeLevel):
        if btnTreeLevel==0:
            return layout_tree,btnTreeLevel
        
        layout_tree.pop() # remove last layout anyway
        return layout_tree,btnTreeLevel-1

# { Editor Button Setting }
class Editor_btnLayout:
    def __init__(self,is_ui,name,text,pyPath,icon,type,tip):
        self.name = name
        self.is_ui = is_ui
        self.text = text
        self.pyPath = pyPath
        self.icon = icon
        self.type = type
        self.tip = tip
    
    def draw_panel(self,btnTreeLevel,layout_tree,Editor):
        active = self.name == Editor.btn_get
        btn_edit_area_func = self.LO_button_edit_box()
        if not self.is_ui :# Button
            self.pn_edit_button(layout_tree,btnTreeLevel,Editor,active,btn_edit_area_func) 
            return layout_tree,btnTreeLevel
        
        if self.type == 0: # label
            self.pn_edit_label(layout_tree,btnTreeLevel,Editor,active,btn_edit_area_func)
            return layout_tree,btnTreeLevel
        
        if self.type == 1: # Panel
            layout_tree,btnTreeLevel = self.pn_edit_panel(layout_tree,btnTreeLevel,Editor,active,btn_edit_area_func)
            return layout_tree,btnTreeLevel
        
        if self.type == 2: # End
            btn_panel,btnTreeLevel = self.pn_edit_end(layout_tree,btnTreeLevel,Editor,active,btn_edit_area_func) 
            return btn_panel,btnTreeLevel

    # button type
    def pn_edit_button(self,layout_tree,btnTreeLevel,Editor,active,btn_edit_area_func):
        layout = layout_tree[btnTreeLevel]
        if not layout:
            return layout_tree,btnTreeLevel
        row = layout.row(align = True)
        # icon
        if self.icon !='NONE':
            icon = self.icon if self.icon in icon_in_blender else 'ERROR'
            textBtn = row.operator("pybtnbox.button_description",text='',icon=icon,emboss=True)
            textBtn.btnName =self.name
            textBtn.text =self.tip
        # pick button
        self.btn_active(row,self.text,active)
        self.btn_operator(row)
        self.btn_order(row,self.name)

        # edit area
        if active:
            btn_edit_area_func(layout,Editor)
        return layout_tree,btnTreeLevel
    #0 label type
    def pn_edit_label(self,layout_tree,btnTreeLevel,Editor,active,btn_edit_area_func):
        layout = layout_tree[btnTreeLevel]
        if not layout:
            return layout_tree,btnTreeLevel
        row1 = layout.row()
        # Icon
        label_icon = self.icon
        if not label_icon in icon_in_blender :
            label_icon ='NONE'
        if label_icon !='NONE':
            row1.label( text=''  ,icon= label_icon )
        # Text 
        col = row1.column(align=True)
        col.alignment='LEFT'
        Txt_list = self.text.split(r'\n')
        label_icon = self.icon if self.icon in icon_in_blender else "NONE"
        for i,txt in enumerate(Txt_list):
            Text = txt if txt!='' else ' '
            col.label( text=Text  ,icon= "NONE" )
        col.alignment='RIGHT'
        
        row1.menu_pie() # for align
        # Edit Button
        row2 = row1.row(align = True)
        self.btn_active(row2,'',active)
        self.btn_operator(row2)
        self.btn_order(row2,self.name)

        if active:
            btn_edit_area_func(layout,Editor)

        return layout_tree,btnTreeLevel

        
    #1 panel type
    def pn_edit_panel(self,layout_tree,btnTreeLevel,Editor,active,btn_edit_area_func):
        layout = layout_tree[btnTreeLevel]
        if not layout :
            layout_tree.append(None)
            return layout_tree,btnTreeLevel+1
        btn_panel = layout.panel(idname=self.name, default_closed=False)
        label_icon = self.icon if self.icon in icon_in_blender else "NONE"
        label_text =self.text if self.text !='' else ' '
        btn_panel[0].label(text=label_text ,icon=label_icon)
        self.btn_active(btn_panel[0],'',active)
        self.btn_operator(btn_panel[0])
        self.btn_order(btn_panel[0],self.name)

        # Edit Area (is self open)
        edit_layout = btn_panel[1]
        if edit_layout:
            if active:
                btn_edit_area_func(edit_layout,Editor)
            row = edit_layout.row(align=True)
            row.label(text='',icon="BLANK1")
            layout_tree.append(row.column())
            return layout_tree,btnTreeLevel+1
        else:
            if active:
               btn_edit_area_func(layout,Editor)
        layout_tree.append(None)
        return layout_tree,btnTreeLevel+1


    #2 return type
    def pn_edit_end(self,layout_tree,btnTreeLevel,Editor,active,btn_edit_area_func):
        layout = layout_tree[btnTreeLevel]
        if layout : # in sub-panel and panel is closed
            row = layout.row(align = True)
            row.label( text=' '  ,icon= "FILE_PARENT" )
            self.btn_active(row,'',active)
            self.btn_operator(row)
            self.btn_order(row,self.name)
            
        # edit area
        if active:
            btn_edit_area_func(layout,Editor)

        if btnTreeLevel >0: # return one level when not on the top level
            layout_tree.pop()
            btnTreeLevel -= 1
        #btnTreeLevel = btnTreeLevel if btnTreeLevel==0 else btnTreeLevel-1
        return layout_tree,btnTreeLevel
    

    @staticmethod
    def LO_button_edit_box():
        def layout_func(Layout,Editor):
            Type_ID = Editor.get( "btn_type",0)
            is_ui = Editor.get( "btn_is_ui",True)
            box = Layout.box()
            column = box.column()
            lo_props(column,Editor,Type_ID,is_ui)
            rowR = box.row()
            rowR.alignment='CENTER'
            rowR.enabled = Editor.btn_name != ''
            rowR.operator("pybtnbox.editor_btn_update",text="Update")
            box.separator(factor=0.1)
            Layout.separator(factor=1)

        def lo_props(Layout,Editor,Type_ID,is_ui):
            if not is_ui: 
                Layout.prop(Editor, "btn_name",text='Name')
                Layout.separator(factor=2.0,type='LINE')
                lo_icon(Layout,Editor.btn_icon)
                Layout.prop(Editor, "btn_icon",text='Icon')
                Layout.prop(Editor, "btn_text",text='Text')
                Layout.prop(Editor, "btn_tip",text='Tip')
                return
            Layout.prop(Editor, "btn_type",text='Type')
            Layout.separator(factor=2.0,type='LINE')
            if Type_ID == 0: 
                lo_icon(Layout,Editor.btn_icon)
                Layout.prop(Editor, "btn_icon",text='Icon')
                Layout.prop(Editor, "btn_text",text='Text')
                return
            if Type_ID == 1: 
                lo_icon(Layout,Editor.btn_icon)
                Layout.prop(Editor, "btn_icon",text='Icon')
                Layout.prop(Editor, "btn_text",text='Text')
                return
            if Type_ID == 2: 
                return

        def lo_icon(Layout,icon_id):
            row = Layout.row()
            row.alignment='CENTER'
            if icon_id in icon_in_blender:
                row.label(icon=icon_id)
                return
            row.alert=True
            row.label(text ='Error Icon',icon='ERROR')
            return
        return layout_func
    
    def btn_active(self,Layout,btn_name,active):
        if not active:
            Layout.operator( "pybtnbox.editor_btn_get"   ,text=btn_name  ,icon= "RADIOBUT_OFF" ).Btn=self.name
        else:
            Layout.operator( "pybtnbox.editor_btn_get_cancel" ,text=btn_name  ,icon= "RADIOBUT_ON" ,depress=True  )

    def btn_operator(self,Layout):
        if not self.is_ui:
            Layout.operator( "pybtnbox.editor_btn_funclist_current" ,text='',icon= "THREE_DOTS"  ).button_path  = self.pyPath
        else:
            Layout.operator( "pybtnbox.editor_layout_del" ,text='',icon= "TRASH"  ).btn_name  = self.name
    
    def btn_order(self,row,Name):
        upBtn = row.operator( "pybtnbox.editor_btn_order_walk"   ,text='',icon= "TRIA_UP"   )
        upBtn.Item  = Name
        upBtn.Walk  = 'up'
        dnBtn = row.operator( "pybtnbox.editor_btn_order_walk"   ,text='',icon= "TRIA_DOWN"   )
        dnBtn.Item  = Name
        dnBtn.Walk  = 'down'
