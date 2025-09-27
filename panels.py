import bpy
import os
from . import modules
PyBtnBox = modules
from . import module_panels
Panel = module_panels


## Main Layout Root Panel
class PYBTNBOX_PT_Main(bpy.types.Panel):
    bl_label = "pyBtnBox"
    bl_region_type = 'UI'
    bl_category = "pyBtnBox"
    icons = None
    area = 'veiw_3d'

    def draw_header(self, context):
        self.layout.label(text = "", icon = "SCRIPT")
    def draw(self, context):
        pass

# [General]
# VIEW_3D
class PYBTNBOX_PT_Main_View( PYBTNBOX_PT_Main ):
    bl_idname = "PYBTNBOX_PT_Main_View"
    bl_space_type = 'VIEW_3D'
    @classmethod
    def poll(cls, context):
        return context.preferences.addons[__package__].preferences.Menus_show[0] 
    def draw(self, context):
        Panel.MenuLayout.draw_panel(self,context,"Menu_area_0")
# IMAGE
class PYBTNBOX_PT_Main_Image( PYBTNBOX_PT_Main ):
    bl_idname = "PYBTNBOX_PT_Main_Image"
    bl_space_type = 'IMAGE_EDITOR'
    @classmethod
    def poll(cls, context):
        nodePanel = context.area.ui_type == "IMAGE_EDITOR"
        menusShow = context.preferences.addons[__package__].preferences.Menus_show[1] 
        return nodePanel and menusShow 
    def draw(self, context):
        Panel.MenuLayout.draw_panel(self,context,"Menu_area_1")
# UV
class PYBTNBOX_PT_Main_Image_UV( PYBTNBOX_PT_Main ):
    bl_idname = "PYBTNBOX_PT_Main_Image_UV"
    bl_space_type = 'IMAGE_EDITOR'
    @classmethod
    def poll(cls, context):
        nodePanel = context.area.ui_type == "UV"
        menusShow = context.preferences.addons[__package__].preferences.Menus_show[2] 
        return nodePanel and menusShow 
    def draw(self, context):
        Panel.MenuLayout.draw_panel(self,context,"Menu_area_2")
# NODE Compositor
class PYBTNBOX_PT_Main_Node_Compositor(PYBTNBOX_PT_Main):
    bl_idname = "PYBTNBOX_PT_Main_Node_Compositor"
    bl_space_type = 'NODE_EDITOR'
    @classmethod
    def poll(cls, context):
        nodePanel = context.area.ui_type == "CompositorNodeTree"
        menusShow = context.preferences.addons[__package__].preferences.Menus_show[3] 
        return nodePanel and menusShow
    def draw(self, context):
        Panel.MenuLayout.draw_panel(self,context,"Menu_area_3")
# NODE Texture
class PYBTNBOX_PT_Main_Node_Tex(PYBTNBOX_PT_Main):
    bl_idname = "PYBTNBOX_PT_Main_Node_Tex"
    bl_space_type = 'NODE_EDITOR'
    @classmethod
    def poll(cls, context):
        nodePanel = context.area.ui_type == "TextureNodeTree"
        menusShow = context.preferences.addons[__package__].preferences.Menus_show[4] 
        return nodePanel and menusShow 
    def draw(self, context):
        Panel.MenuLayout.draw_panel(self,context,"Menu_area_4")
# NODE Geometry
class PYBTNBOX_PT_Main_Node_Geo(PYBTNBOX_PT_Main):
    bl_idname = "PYBTNBOX_PT_Main_Node_Geo"
    bl_space_type = 'NODE_EDITOR'
    @classmethod
    def poll(cls, context):
        nodePanel = context.area.ui_type == "GeometryNodeTree"
        menusShow = context.preferences.addons[__package__].preferences.Menus_show[5] 
        return nodePanel and menusShow
    def draw(self, context):
        Panel.MenuLayout.draw_panel(self,context,"Menu_area_5")

# NODE Shader
class PYBTNBOX_PT_Main_Node_Shader(PYBTNBOX_PT_Main):
    bl_idname = "PYBTNBOX_PT_Main_Node_Shader"
    bl_space_type = 'NODE_EDITOR'
    @classmethod
    def poll(cls, context):
        nodePanel = context.area.ui_type == "ShaderNodeTree"
        menusShow = context.preferences.addons[__package__].preferences.Menus_show[6] 
        return nodePanel and menusShow
    def draw(self, context):
        Panel.MenuLayout.draw_panel(self,context,"Menu_area_6")

# SEQUENCE_EDITOR
class PYBTNBOX_PT_Main_Video(PYBTNBOX_PT_Main):
    bl_idname = "PYBTNBOX_PT_Main_Video"
    bl_space_type = 'SEQUENCE_EDITOR'
    @classmethod
    def poll(cls, context):
        return context.preferences.addons[__package__].preferences.Menus_show[7] 
    def draw(self, context):
        Panel.MenuLayout.draw_panel(self,context,"Menu_area_7")
# [Animation]
# DOPESHEET_EDITOR
class PYBTNBOX_PT_Main_Dope( PYBTNBOX_PT_Main ):
    bl_idname = "PYBTNBOX_PT_Main_Dope"
    bl_space_type = 'DOPESHEET_EDITOR'
    @classmethod
    def poll(cls, context):
        nodePanel = context.area.ui_type == "DOPESHEET"
        menusShow = context.preferences.addons[__package__].preferences.Menus_show[8] 
        return nodePanel and menusShow
    def draw(self, context):
        Panel.MenuLayout.draw_panel(self,context,"Menu_area_8")
# [Animation]
# GRAPH_EDITOR
class PYBTNBOX_PT_Main_Graph_Fcurves( PYBTNBOX_PT_Main ):
    bl_idname = "PYBTNBOX_PT_Main_Graph_Fcurves"
    bl_space_type = 'GRAPH_EDITOR'
    @classmethod
    def poll(cls, context):
        nodePanel = context.area.ui_type == "FCURVES"
        menusShow = context.preferences.addons[__package__].preferences.Menus_show[9] 
        return nodePanel and menusShow
    def draw(self, context):
        Panel.MenuLayout.draw_panel(self,context,"Menu_area_9")
# GRAPH_EDITOR
class PYBTNBOX_PT_Main_Graph_Drivers( PYBTNBOX_PT_Main ):
    bl_idname = "PYBTNBOX_PT_Main_Graph_Drivers"
    bl_space_type = 'GRAPH_EDITOR'
    @classmethod
    def poll(cls, context):
        nodePanel = context.area.ui_type == "DRIVERS"
        menusShow = context.preferences.addons[__package__].preferences.Menus_show[10] 
        return nodePanel and menusShow
    def draw(self, context):
        Panel.MenuLayout.draw_panel(self,context,"Menu_area_10")
# NLA_EDITOR
class PYBTNBOX_PT_Main_NLA( PYBTNBOX_PT_Main ):
    bl_idname = "PYBTNBOX_PT_Main_NLA"
    bl_space_type = 'NLA_EDITOR'
    @classmethod
    def poll(cls, context):
        return context.preferences.addons[__package__].preferences.Menus_show[11] 
    def draw(self, context):
        Panel.MenuLayout.draw_panel(self,context,"Menu_area_11")
# [Scripting]
# TEXT_EDITOR
class PYBTNBOX_PT_Main_Script( PYBTNBOX_PT_Main ):
    bl_idname = "PYBTNBOX_PT_Main_Script"
    bl_space_type = 'TEXT_EDITOR'
    @classmethod
    def poll(cls, context):
        return context.preferences.addons[__package__].preferences.Menus_show[12] 
    def draw(self, context):
        Panel.MenuLayout.draw_panel(self,context,"Menu_area_12")
'''
# DOPESHEET_EDITOR
class PYBTNBOX_PT_Main_Dope_Timelime( PYBTNBOX_PT_Main ):
    bl_idname = "PYBTNBOX_PT_Main_Dope_Timelime"
    bl_space_type = 'DOPESHEET_EDITOR'
    @classmethod
    def poll(cls, context):
        nodePanel = context.area.ui_type == "TIMELINE"
        menusShow = context.preferences.addons[__package__].preferences.Menus_show[9] 
        return nodePanel and menusShow
    def draw(self, context):
        Panel.MenuLayout.draw_panel(self,context,"Menu_area_13")
'''


#==================
#==  Edit Panel  ==
#==================

# Menu Select
class PYBTNBOX_PT_Editor_Menu(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_space_type = 'TEXT_EDITOR'
    bl_region_type = 'UI'
    bl_category = "pyBtnBox Edit"
    bl_label = ''
    bl_idname = "PYBTNBOX_PT_Editor_Menu"
    bl_options = {'HEADER_LAYOUT_EXPAND'}

    def draw_header(self, context):
        layout = self.layout
        layout.label(text='pyBtnBox editor',icon='TOOL_SETTINGS')
        return
        

    def draw(self, context):
        Editor = context.scene.pybtnbox_prop_editor
        MenuName = Editor.menu
        layout = self.layout
        # If Not Found
        if PyBtnBox.Root.path()=='':
            box = layout.box()
            box.alignment='CENTER'
            box.label(text='Not found root folder',icon='ERROR')
            return
        Menu = PyBtnBox.Menu.from_menu_name(Editor.menu)
        row = layout.row()
        Icon = Menu.icon if PyBtnBox.is_icon_in_blender(Menu.icon) else 'NONE'
        row.prop(Editor,'menu',text='',icon=Icon)
        row.operator("pybtnbox.editor_menu_funclist_current",text='', icon = "THREE_DOTS")
        
        if MenuName =='':
            return
        if not MenuName in PyBtnBox.Root.menu_list():
            box = layout.box()
            row = box.row()
            row.alignment='CENTER'
            row.label(text='Not found this menu in folder',icon='ERROR')
            return
        layout.separator(factor=2.0,type="LINE")

        # Setting Area
        box = layout.box()
        row = box.row()
        row.alignment='CENTER'
        Icon = Editor.menu_icon
        if Icon in Panel.icon_in_blender:
            row.label(text='',icon=Icon)
        else :
            row.alert = True
            row.label(text='icon error',icon='ERROR')
        
        row = box.row()
        row.prop(Editor, "menu_name",text='Name')
        row = box.row()
        row.prop(Editor, "menu_icon",text='Icon')

        # Set Used Areas
        row = box.row()
        areaBox = row.box()
        areaPanel = areaBox.panel('menu_area_panel',default_closed=True)
        areaPanel[0].alignment='CENTER'
        areaPanel[0].label(text='Searched In')
        if areaPanel[1]:
            areaBox_col = areaPanel[1].column(align=True)
            for i in range(13):
                areaBox_col.prop(Editor,'menu_useAreas',index=i,
                                 text=Panel.AreaData[i][0],
                                 icon=Panel.AreaData[i][1])
        # Update Button
        row = box.row()
        row.alignment='CENTER'
        row.operator("pybtnbox.editor_menu_update",text='Update')

        box.separator(factor=0.05)


class PYBTNBOX_PT_Editor_Button(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_space_type = 'TEXT_EDITOR'
    bl_region_type = 'UI'
    bl_category = "pyBtnBox Edit"
    bl_label = "Buttons Edit"
    bl_idname = "PYBTNBOX_PT_Editor_Button"
    bl_order = 1
    bl_options = {'HEADER_LAYOUT_EXPAND','DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        Menu = context.scene.pybtnbox_prop_editor.menu
        Menus = PyBtnBox.Root.menu_list()
        return Menu in Menus
    
    def draw_header(self, context):
        layout = self.layout
        layout.alignment = 'RIGHT'
        layout.operator("pybtnbox.editor_btn_funclist_add",text='', icon = "PLUS")

    
    def draw(self, context):
        Editor = context.scene.pybtnbox_prop_editor
        Menu = PyBtnBox.Menu.from_menu_name(Editor.menu)
        layout_tree = [self.layout]
        menuData = Menu.json
        pyBtns = [btn for btn in menuData.keys() if btn != '__menuAttributes__']
        btnTreeLevel =0
        for pyBtn in pyBtns :
            btnData = menuData.get(pyBtn,None)
            if not btnData:
                continue
            btnLO = Panel.Editor_btnLayout(
                                name   = pyBtn,
                                text   = btnData.get('text',''),
                                pyPath = os.path.join(Menu.menu_path,f'{pyBtn}.py'),
                                icon   = btnData.get('icon','NONE'),
                                type   = btnData.get('type',0),
                                tip    = btnData.get('tip',''),
                                )
            
            layout_tree,btnTreeLevel = btnLO.draw_panel(btnTreeLevel,layout_tree,Editor)

class_list = [
    # [ Main Panels ]
    PYBTNBOX_PT_Main_View,
    PYBTNBOX_PT_Main_Image,
    PYBTNBOX_PT_Main_Image_UV,
    PYBTNBOX_PT_Main_Node_Compositor,
    PYBTNBOX_PT_Main_Node_Tex,
    PYBTNBOX_PT_Main_Node_Geo,
    PYBTNBOX_PT_Main_Node_Shader,
    PYBTNBOX_PT_Main_Video,
    PYBTNBOX_PT_Main_Dope,
    PYBTNBOX_PT_Main_Graph_Fcurves,
    PYBTNBOX_PT_Main_Graph_Drivers,
    PYBTNBOX_PT_Main_NLA,
    PYBTNBOX_PT_Main_Script,
    #PYBTNBOX_PT_Main_Dope_Timelime,

    # [ Edit Panel ]
    PYBTNBOX_PT_Editor_Menu,
    PYBTNBOX_PT_Editor_Button
]
def register():
    for cls in class_list:
        bpy.utils.register_class(cls)


def unregister():
    class_list.reverse()
    for cls in class_list:
        bpy.utils.unregister_class(cls)