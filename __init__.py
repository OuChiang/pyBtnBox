import bpy
import os
import importlib

# Preferences
class PyBtnBox_Preferences(bpy.types.AddonPreferences):
    bl_idname = __package__
    
    root_path : bpy.props.StringProperty(
        name="Example File Path",
        default=r'D:\\pybtnbox_menus\\',
        subtype='DIR_PATH',
    )

    Menus_show : bpy.props.BoolVectorProperty(
        name="Panel Use",
        size=14,
        default=(True,True,True,True,True,True,True,
                 True,True,True,True,True,True,True)
        )
    
    def draw(self, context):
        layout = self.layout

        # Root Path 
        layout.prop(self, "root_path",text='Root Folder Path')
        row = layout.row()
        rootPath = self.root_path
        dir_base_name = os.path.basename(os.path.dirname(rootPath))
        def check_is_error(layout):
            is_errors = False
            if rootPath=='':
                row = layout.row()
                info_txt = 'For data security reasons, the root folder must be named start with \"pybtnbox_menus\"'
                row.label(text=info_txt, icon='INFO')
                return True
            if not dir_base_name.startswith('pybtnbox_menus'):
                row = layout.row()
                row.alert=True
                info_txt = 'The folder name must start with \"pybtnbox_menus\"'
                row.label(text=info_txt, icon='ERROR')
                is_errors = True
            if not os.path.exists(rootPath):
                row = layout.row()
                row.alert=True
                row.label(text='The folder not found', icon='ERROR')
                is_errors = True
            return is_errors
        if not check_is_error(layout):
            col = row.column(align=True)
            col.label(text='Root Folder Path Fine', icon='CHECKMARK')
            col.label(text='You can edit Menus/Buttons in :', icon='INFO')
            col.label(text='Text_Editor > Sidebar > pyBtnBox Edit', icon='BLANK1')

        # Show Area
        Area_data = [
            ['3D Viewport','VIEW3D'],
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
        useAreas = layout.panel('use_area',default_closed =True)
        useAreas[0].label(text='Area')
        if useAreas[1]:
            col_areas =useAreas[1].column(align=True)
            for i,velues in enumerate(Area_data):
                col_areas.prop(self,'Menus_show',index=i,text=velues[0],icon=velues[1])



class_list = [
    'properties',
    'operators',
    'panels',
]
def register():
    bpy.utils.register_class(PyBtnBox_Preferences)
    for cls in class_list:
        param = importlib.import_module(f'.{cls}',package=__name__)
        param.register()


def unregister():
    class_list.reverse()
    for cls in class_list:
        param = importlib.import_module(f'.{cls}',package=__name__)
        param.unregister()
    bpy.utils.unregister_class(PyBtnBox_Preferences)