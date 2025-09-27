import bpy
import os

from . import modules
PyBtnBox = modules

def menu_search_filter(self,context,edit_text,menu_id):
    output = []
    root = PyBtnBox.Root()
    for menuName in root.menu_list():
        menu = PyBtnBox.Menu.from_menu_name(menuName) 
        if menu.area[menu_id]:
            output.append(menuName)
    #output = [d for d in root.menu_list() if os.path.isdir( os.path.join(root.path,d))]
    return output
    
# Properties
class PYBTNBOX_Prop(bpy.types.PropertyGroup):
    def add_menu_enum(menu_id):
        return  bpy.props.StringProperty(
            name=f"Menu_{menu_id}" ,
            description="Select Menu",
            search = lambda self,context,edit_text:menu_search_filter(self,context,edit_text,menu_id),
            search_options ={'SUGGESTION'}
            )
    Menu_area_0 : add_menu_enum(0)
    Menu_area_1 : add_menu_enum(1)
    Menu_area_2 : add_menu_enum(2)
    Menu_area_3 : add_menu_enum(3)
    Menu_area_4 : add_menu_enum(4)
    Menu_area_5 : add_menu_enum(5)
    Menu_area_6 : add_menu_enum(6)
    Menu_area_7 : add_menu_enum(7)    
    Menu_area_8 : add_menu_enum(8)
    Menu_area_9 : add_menu_enum(9)
    Menu_area_10 : add_menu_enum(10)
    Menu_area_11 : add_menu_enum(11)
    Menu_area_12 : add_menu_enum(12)
    #Menu_area_13 : add_menu_enum(13)


def menu_update(self,context):
    folder_name = self.menu
    if folder_name not in PyBtnBox.Root().menu_list():
        return None
    
    menu = PyBtnBox.Menu.from_menu_name(folder_name)
    self.menu_name = menu.name
    self.menu_icon = menu.icon
    Editor_Areas = menu.area
    for i in range(14):
        self.menu_useAreas[i] = Editor_Areas[i]
    
    # Update Btn Edit
    self.btn_get=''
    return None

def menu_search(self, context, edit_text):
    return PyBtnBox.Root().menu_list()


# PyBtnBox Editor Props
class PYBTNBOX_Prop_Editor(bpy.types.PropertyGroup):

    menu : bpy.props.StringProperty(
        name="Menu",
        description='Select Edit Menu',
        update = menu_update,
        search = menu_search,
        search_options ={'SUGGESTION'}
        )
    
    menu_name: bpy.props.StringProperty(name="Menu Rename",
                                        description="Reset Menu Name",
                                        default='')
    menu_icon: bpy.props.StringProperty(name="Menu Icon",
                                        description="Reset Menu Icon",
                                        default='')
    menu_useAreas_option : bpy.props.BoolProperty(name="Areas Use",
                                                  description="Show Menu Reset Areas",
                                                  default=False)
    menu_useAreas : bpy.props.BoolVectorProperty(
        name="Areas Use",
        description="Reset Menu Used Areas",
        size=14
        )

    # Button Edit Props
    btn_get: bpy.props.StringProperty(name="Btn Name",
                                      description="Show Button In Edit Options",
                                      default="")
    btn_name: bpy.props.StringProperty(name="Btn Rename",
                                       description="Reset The python file Name",
                                       default="")
    btn_text: bpy.props.StringProperty(name="Btn Text",
                                       description="Reset The Button Text", 
                                       default="")
    btn_icon: bpy.props.StringProperty(name="Btn Icon", 
                                       description="Reset The Button Icon", 
                                       default="")
    btn_tip: bpy.props.StringProperty(name="Btn Tip", 
                                       description="Reset The Button Tip", 
                                       default="")
    btn_type : bpy.props.EnumProperty(
        name="Btn Type", 
        description="Type For UILayout", 
        items = [('0','button','','PLAY',0),
                 ('1','panel','','DOWNARROW_HLT',1),
                 ('2','return','','FILE_PARENT',2),
                 ('3','label','','SMALL_CAPS',3)],
        default='0'
        )
class_list = []
def register():
    bpy.utils.register_class(PYBTNBOX_Prop)
    bpy.utils.register_class(PYBTNBOX_Prop_Editor)
    bpy.types.Scene.pybtnbox_prop = bpy.props.PointerProperty(type=PYBTNBOX_Prop)
    bpy.types.Scene.pybtnbox_prop_editor = bpy.props.PointerProperty(type=PYBTNBOX_Prop_Editor)
    
    for cls in class_list:
        cls.register()


def unregister():

    class_list.reverse()
    for cls in class_list:
        cls.unregister()
    del bpy.types.Scene.pybtnbox_prop
    del bpy.types.Scene.pybtnbox_prop_editor
    bpy.utils.unregister_class(PYBTNBOX_Prop)
    bpy.utils.unregister_class(PYBTNBOX_Prop_Editor)