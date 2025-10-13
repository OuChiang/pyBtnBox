import bpy
import os
import json

AreaData = [['3D Viewport','VIEW3D'],
            ['Image Editor','IMAGE'],
            ['UV Editor','UV'],
            ['Compositor','NODE_COMPOSITING'],
            ['Texture Node Editor','NODE_TEXTURE'],
            ['Geometry Node Editor','GEOMETRY_NODES'],
            ['Shader Editor','SHADING_RENDERED'],
            ['Video Sequencer','SEQUENCE'],
            ['Dope Sheet','ACTION'],
            ['Timeline','TIME'],
            ['Graph Editor','GRAPH'],
            ['Drivers','DRIVER'],
            ['Nonlinear Animation','NLA'],
            ['Text Editor','TEXT']]
def is_icon_in_blender(iconName):
    items = bpy.types.UILayout.bl_rna.functions["prop"].parameters["icon"].enum_items.keys()
    
    return iconName in items

def get_script_folder_root():
    addon_prefs = bpy.context.preferences.addons[__package__].preferences
    if not addon_prefs:
        return ''
    
    rootPath = getattr(addon_prefs,'root_path')
    dir_base_name = os.path.basename(os.path.dirname(rootPath))
    if not dir_base_name.startswith('pybtnbox_menus'):
        return ''
    if not os.path.exists(rootPath):
        return ''
    return rootPath

class Root:
    @staticmethod
    def path():
        return get_script_folder_root()
    @staticmethod
    def menu_list():
        output_list = []
        if not os.path.exists(Root.path()):
            return output_list
        for dirNm in os.listdir( Root.path() ):
            menu_path = os.path.join(Root.path(),dirNm)
            if os.path.isdir( menu_path):
                output_list.append(dirNm)
        return output_list


class Menu:
    def __init__(self,rootPath,menuName,menuPath,jsonPath,menuJson,menuAttrs,menuIcon,menuArea):
        self.root_path = rootPath
        self.name = menuName
        self.menu_path = menuPath
        self.json_path = jsonPath
        self.json = menuJson
        self.attr = menuAttrs
        self.icon = menuIcon
        self.area = menuArea

    @classmethod
    def from_menu_name(cls,menuName):
        default_icon = 'NONE'
        default_area = [True for i in range(14)]
        default_data = {'icon':default_icon,'area':default_area}
        default_json = {'__menuAttributes__':default_data}
        # Path Check
        rootPath = get_script_folder_root()
        if not os.path.exists(rootPath):
            return cls(rootPath,menuName,'','',default_json,default_data,default_icon,default_area)
        
        menuPath = os.path.join(rootPath,menuName)
        if not os.path.exists(menuPath):
            return cls(rootPath,menuName,'','',default_json,default_data,default_icon,default_area)
        
        jsonPath = os.path.join(menuPath,'_menuData.json')
        if not os.path.exists(jsonPath):
            return cls(rootPath,menuName,menuPath,'',default_json,default_data,default_icon,default_area)
        with open( jsonPath, 'r') as f: 
            data = json.load(f)
        
        
        try: # Attrs Check
            menuAttrs = data['__menuAttributes__']
            menuIcon = menuAttrs['icon']
            menuArea = menuAttrs['area']
        except :
            cls.data_update()
        
        return cls(rootPath,menuName,menuPath,jsonPath,data,menuAttrs,menuIcon,menuArea)

    def data_update(self):
        # Check dose json exist
        if '' in [self.root_path,self.menu_path]:
            return
        if self.json_path =='': 
            old_all_data ={}
            jsonPath = os.path.join(self.menu_path,'_menuData.json')
            return
        else:
            old_all_data = self.json
            jsonPath = self.json_path
        
        # Menu Atrributes
        old_menu_attrs = old_all_data.get('__menuAttributes__',None)
        if not old_menu_attrs:
            old_menu_icon = 'FILE_FOLDER'
            old_menu_area = [True for i in range(14)]
        else:
            old_menu_icon = old_menu_attrs.get('icon','FILE_FOLDER')
            old_menu_area = old_menu_attrs.get('area',[True for i in range(14)])

        new_all_data = {'__menuAttributes__':{
            'icon' : old_menu_icon,
            'area' : old_menu_area
        }}


        # refresh python files in menu
        old_all_keys = old_all_data.keys()
        pyFiles = self.get_pyFiles(mode='base')
        
        not_in_list = [f for f in pyFiles if f not in old_all_keys]
        order_files = [f for f in old_all_keys if f in pyFiles]
        

        for btnName,btnData in old_all_data.items():
            # If Button is UI Type
            if btnData.get('is_ui',False):
                new_all_data[btnName] = {
                        'is_ui':True,
                        'type':btnData.get('type',0),
                        'icon':btnData.get('icon',"BLANK1"),
                        'text':btnData.get('text',btnName),
                }
                continue
            # If Button is already existed python file
            if btnName in order_files:
                new_all_data[btnName] = {
                        'is_ui':btnData.get('btn_is_ui',False),
                        'icon':btnData.get('icon',"BLANK1"),
                        'text':btnData.get('text',btnName),
                        'tip':btnData.get('tip',btnName),
                }
                continue
        for btnName in not_in_list:
                new_all_data[btnName] = {
                        'is_ui':False,
                        'icon':"BLANK1",
                        'text':btnName,
                        'tip':btnName,
                }
        # output json
        json_data = json.dumps(new_all_data, indent=4)
        with open( jsonPath , 'w+') as f:
            f.write(json_data)
        return 'DONE'
    
    def get_pyFiles(self,mode):
        output_list = []
        if self.menu_path=='':
            return output_list
        
        for file in os.listdir( self.menu_path ):
            if not file.endswith('.py'):
                continue
            if mode == 'name':
                output_list.append(file)
            if mode == 'base':
                output_list.append(file[:-3])
            if mode == 'path':
                os.path.join( self.menu_path,file )
        return output_list
    

