import bpy
from bpy_extras.io_utils import ImportHelper,ExportHelper
import os
import shutil

from . import modules
PyBtnBox = modules



#========================
#=== Grobal Settings  ===
#========================

class PYBTNBOX_OT_ReloadData(bpy.types.Operator):
    """Reload All PyBtnBox Data"""
    bl_idname = "pybtnbox.reload_data"
    bl_label = "Reload Data"
    def execute(self, context):
        Menus = PyBtnBox.Root.menu_list()
        for MenuName in Menus:
            Menu = PyBtnBox.Menu.from_menu_name(MenuName)
            Menu.data_update()
        
        return {'FINISHED'}


#===========================
#=== Main PyBtnBox Panel ===
#===========================

# Button Execute
class PYBTNBOX_OT_Btn_Execute(bpy.types.Operator):
    """Execute Python File"""
    bl_idname = "pybtnbox.button_execute"
    bl_label = "Button"
    File : bpy.props.StringProperty(default="")
    
    def execute(self, context):
        file_path = self.File
        if os.path.isfile(file_path):
            bpy.utils.execfile(filepath = file_path)
            message = 'File Executed'
            self.report({'OPERATOR'}, message)
        else:
            message = "File Not Found"
            self.report({'ERROR'}, message)

        return {'FINISHED'}

# Button Description
class PYBTNBOX_OT_Btn_Description(bpy.types.Operator):
    """Show Button Description"""
    bl_idname = "pybtnbox.button_description"
    bl_label = 'Info'
    bl_description = 'Button Info'
    btnName: bpy.props.StringProperty(default="")
    text: bpy.props.StringProperty(default="")

    def execute(self, context):
        return {'FINISHED'}
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_popup(self)

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        for t in self.text.split('\\n'):
            row = col.row()
            row.label(text=t)



#=========================
#===    Edit Panel     ===
#=========================

# [ Drop-down list ] Menu Edit
class PYBTNBOX_OT_Editor_Menu_Function_List_Current(bpy.types.Operator):
    """Functions List For Current Menu"""
    bl_idname = "pybtnbox.editor_menu_funclist_current"
    bl_label = "Menu Factions"  

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_popup(self)
    
    def draw(self, context):
        layout = self.layout
        layout.label(text='Current Menu')
        layout.operator("pybtnbox.editor_menu_new" ,text='New Empty Menu',icon= 'NEWFOLDER' )
        layout.operator("pybtnbox.menu_open_folder" ,text='Open Menus Folder',icon= 'FILEBROWSER' )
        layout.operator("pybtnbox.editor_menu_del",text="Remove Menu",icon='TRASH')

## --- Menus
# Menu Add
class PYBTNBOX_OT_Editor_Menu_New(bpy.types.Operator):
    """Add An Empty New Menu"""
    bl_idname = "pybtnbox.editor_menu_new"
    bl_label = "Add New Menu"

    def execute(self, context):
        menusPath = PyBtnBox.Root.path()
        NameBase = 'newMenu'
        nameNumber = 0
        
        newMenuPath = os.path.join(menusPath , NameBase + str(nameNumber))
        while os.path.exists(newMenuPath):
            nameNumber += 1
            newMenuPath = os.path.join(menusPath , NameBase + str(nameNumber))
        os.makedirs(newMenuPath)
        Menu = PyBtnBox.Menu.from_menu_name(f'{NameBase}{str(nameNumber)}')
        json_path = os.path.join(Menu.menu_path,f'_menuData.json')
        default_json = {
            '__menuAttributes__':{
            'icon':"SCRIPT",
            'area':[True for i in range(14)]
            }
            }
        import json
        json_data = json.dumps(default_json, indent=4)
        with open( json_path , 'w+') as f:
            f.write(json_data)
        context.scene.pybtnbox_prop_editor.menu = NameBase + str(nameNumber)
        return {'FINISHED'}


# Open Menu Folder
class PYBTNBOX_OT_Menu_Open_Folder(bpy.types.Operator):
    """Open Current Menu Forlder"""
    bl_idname = "pybtnbox.menu_open_folder"
    bl_label = "Open Menu Folder"
    def execute(self, context):
        os.startfile( self.Path )
        return {'FINISHED'}
    
    def execute(self, context):
        folder_path = PyBtnBox.Root.path()
        if folder_path!='':
            os.startfile( folder_path )
        return {'FINISHED'}


# Menu Remove
class PYBTNBOX_OT_Editor_Menu_Del(bpy.types.Operator):
    """Delete Current Menu"""
    bl_idname = "pybtnbox.editor_menu_del"
    bl_label = "Remove Menu"
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
    def execute(self, context):
        Editor = context.scene.pybtnbox_prop_editor
        Menu = PyBtnBox.Menu.from_menu_name(Editor.menu)

        menu_list = PyBtnBox.Root.menu_list()
        Menu_id = menu_list.index(Editor.menu)
        
        try:
            shutil.rmtree(Menu.menu_path)
            self.report({'INFO',},f'{Editor.menu} is already deleted')

        except PermissionError:
            self.report({'ERROR',},f'PermissionError: [WinError 5] Access is denied : {Menu.menu_path}')

        # re-set order in list
        menu_list = PyBtnBox.Root.menu_list()
        if not menu_list:
            Editor.menu = ''
        else :
            Editor.menu = menu_list[Menu_id-1]
        return {'FINISHED'}
    
    def draw(self, context):
        Editor = context.scene.pybtnbox_prop_editor

        MenuName = Editor.menu
        layout = self.layout

        row = layout.row()
        row.alert = True
        row.label(text ='Delete Cannot Be Undo,Are You Sure?',icon = 'ERROR')

        row = layout.row()
        row.label(text=MenuName, icon="TRASH")


# [ Menu Editor ]
# Menu Update
class PYBTNBOX_OT_Editor_Menu_Update(bpy.types.Operator):
    """Save Edited Settings Of Current Menu """
    bl_idname = "pybtnbox.editor_menu_update"
    bl_label = "Rename Menu"
    @classmethod
    def poll(cls, context):
        Editor = context.scene.pybtnbox_prop_editor
        return Editor.menu_name
    def execute(self, context):
        Editor = context.scene.pybtnbox_prop_editor
        menu_name = Editor.menu
        Menu = PyBtnBox.Menu.from_menu_name(Editor.menu)
        # Save Menu Settings
        menuJson = Menu.json
        menuJson['__menuAttributes__']['icon'] = Editor.menu_icon
        menuJson['__menuAttributes__']['area'] = list(Editor.menu_useAreas)
        # output json
        import json
        json_data = json.dumps(menuJson, indent=4)
        with open( Menu.json_path , 'w+') as f:
            f.write(json_data)

        OldNamePath = os.path.join(Menu.root_path , menu_name)
        NewName = Editor.menu_name
        NewNamePath = os.path.join(Menu.root_path , NewName)
        
        os.rename(OldNamePath,NewNamePath)

        Editor.menu = NewName
        
        self.report({'OPERATOR',},f'Menu Saved : {NewName}')
        return {'FINISHED'}
    

#--------------
#--- Button ---
#--------------

# [ Drop-down list ] Add Button
class PYBTNBOX_OT_Editor_Btn_Function_List_Add(bpy.types.Operator):
    """Function list for button creating"""
    bl_idname = "pybtnbox.editor_btn_funclist_add"
    bl_label = "Create Button"

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_popup(self)
    
    def draw(self, context):
        layout = self.layout
        layout.label(text='Add Button')
        layout.operator("pybtnbox.add_btn",text='Empty Button',icon='FILE_NEW')
        layout.operator("pybtnbox.editor_btn_load_to_text_editor",text='From Current Text',icon='TEXT')

        layout.separator(factor=1.0, type='LINE')
        layout.label(text='Add Layout')
        layout.operator("pybtnbox.editor_layout_add",text='New Layout',icon='ALIGN_LEFT')
        
        
# Add New
class PYBTNBOX_OT_Editor_Btn_New(bpy.types.Operator):
    """Add A New Button"""
    bl_idname = "pybtnbox.add_btn"
    bl_label = "Add New Btn"

    def execute(self, context):
        Editor = context.scene.pybtnbox_prop_editor
        Menu = PyBtnBox.Menu.from_menu_name(Editor.menu)

        num = 0
        newPath = os.path.join(Menu.menu_path , f'newBtn_{num}.py')
        while os.path.exists(newPath):
            num+=1
            newPath = os.path.join(Menu.menu_path , f'newBtn_{num}.py')

        with open( newPath , 'w+') as f:
            f.write('')
        
        Menu.data_update()
        return {'FINISHED'}
    
# Add From current Text
class PYBTNBOX_OT_Editor_Btn_LoadToTextEditor(bpy.types.Operator):
    """Add New Button From Current Text"""
    bl_idname = "pybtnbox.editor_btn_load_to_text_editor"
    bl_label = "Add From current Text"

    def execute(self, context):
        Editor = context.scene.pybtnbox_prop_editor
        Menu = PyBtnBox.Menu.from_menu_name(Editor.menu)


        # Get Base Name
        currentText = context.space_data.text
        if not currentText:
            return {'CANCELLED'}
        base_name  = currentText.name
        if base_name.endswith('.py'):
            base_name  = base_name[:-3]
        
        # Add New Button
        num = 0
        newPath = os.path.join(Menu.menu_path , f'{base_name}.py')
        while os.path.exists(newPath):
            num+=1
            newPath = os.path.join(Menu.menu_path , f'{base_name}_{num}.py')

        bpy.ops.text.save_as(filepath=newPath)
        Menu.data_update()
        return {'FINISHED'}


# ---------------------
# --- Button Editor ---
# ---------------------
# Get Button
class PYBTNBOX_OT_Editor_Btn_Get(bpy.types.Operator):
    """Edit This Button"""
    bl_idname = "pybtnbox.editor_btn_get"
    bl_label = "Editor Get Btn"
    Btn : bpy.props.StringProperty(default="")

    def execute(self, context):
        Editor = context.scene.pybtnbox_prop_editor
        Menu = PyBtnBox.Menu.from_menu_name(Editor.menu)
        Data = Menu.json
        BtnData = Data.get(self.Btn,None)
        if not BtnData:
            return {'FINISHED'}
        
        BtnIsUI = BtnData.get("is_ui",False)
        BtnType = BtnData.get("type",0)
        BtnText = BtnData.get("text",'')
        BtnIcon = BtnData.get("icon",'NONE')
        BtnTip  = BtnData.get("tip",'')
        btnEd = context.scene.pybtnbox_prop_editor
        btnEd.btn_get  =self.Btn
        btnEd.btn_name =self.Btn
        btnEd.btn_text =BtnText
        btnEd.btn_icon =BtnIcon
        btnEd.btn_tip  =BtnTip
        btnEd.btn_is_ui = BtnIsUI
        btnEd.btn_type =str(BtnType)
        btnEd.menu_del_bool = False
        btnEd.btn_del_bool = False
        return {'FINISHED'}

# Get Button Cancel 
class PYBTNBOX_OT_Editor_Btn_Get_Cancel(bpy.types.Operator):
    """Cancel Button Edit"""
    bl_idname = "pybtnbox.editor_btn_get_cancel"
    bl_label = "Button Editor Cancel"
    def execute(self, context):
        context.scene.pybtnbox_prop_editor.btn_get=''
        return {'FINISHED'}



# Button Update
class PYBTNBOX_OT_Editor_Btn_Update(bpy.types.Operator):
    """Save Edited Button Settings"""
    bl_idname = "pybtnbox.editor_btn_update"
    bl_label = "Editor Reset Btn"

    def execute(self, context):
        Editor = context.scene.pybtnbox_prop_editor
        Menu  = PyBtnBox.Menu.from_menu_name(Editor.menu)

        menuData = Menu.json
        newData = {}
        for btnName,old_data in menuData.items():
            # Is Other Btn
            if btnName != Editor.btn_get:
                newData[btnName] = old_data
                continue
            
            # Update UI
            if Editor.get('btn_is_ui'):
                newData[btnName]={}
                newData[btnName]['is_ui']=True
                newData[btnName]['type']=Editor.get('btn_type',0)
                newData[btnName]['text']=Editor.get('btn_text','')
                newData[btnName]['icon']=Editor.get('btn_icon','NONE')
                continue
            # Update Btn
            old_name = Editor.btn_get
            new_name = Editor.btn_name
            if old_name != new_name: 
                oldPyPath = os.path.join(Menu.menu_path,f'{old_name}.py')
                newPyPath = os.path.join(Menu.menu_path,f'{new_name}.py')
                os.rename(oldPyPath,newPyPath)
            newData[new_name] = {}
            newData[new_name]['is_ui']=False
            newData[new_name]['text']=Editor.get('btn_text','')
            newData[new_name]['icon']=Editor.get('btn_icon','NONE')
            newData[new_name]['tip'] =Editor.get('btn_tip','')

        import json
        json_data = json.dumps(newData, indent=4)
        with open( Menu.json_path , 'w+') as f:
            f.write(json_data)
        
        # Reload
        Editor.btn_get = ''
        self.report({'OPERATOR',},f'Button Saved : {Editor.btn_name}')
        return {'FINISHED'}



# Order walk( up/down )
class PYBTNBOX_OT_Editor_Btn_OrderWalk(bpy.types.Operator):
    """Button Position Walk Up Or Down"""
    bl_idname = "pybtnbox.editor_btn_order_walk"
    bl_label = "Button Walk"
    Walk : bpy.props.StringProperty(default="up")
    Item : bpy.props.StringProperty(default="")
    def execute(self, context):
        Editor = context.scene.pybtnbox_prop_editor
        Menu = PyBtnBox.Menu.from_menu_name(Editor.menu)
        menuData = Menu.json
        btnList = [ k for k in menuData.keys()]
        Index=0
        for i in range(len(btnList)):
            if btnList[i] == self.Item:
                Index=i
        if 0 <= Index < len(btnList):
            if   self.Walk =='up':
                btnList.pop(Index)
                btnList.insert( Index-1 , self.Item )
            if self.Walk =='down':
                btnList.pop(Index)
                btnList.insert( Index+1 , self.Item )
        jsonData ={}
        for menuNm in btnList:
            jsonData[menuNm] = menuData[menuNm]
        
        import json
        json_data = json.dumps(jsonData, indent=4)
        with open( Menu.json_path , 'w+') as f:
            f.write(json_data)
        return {'FINISHED'}


# [ Drop-down list ] Edit Current Button
class PYBTNBOX_OT_Editor_Btn_Function_List_Current(bpy.types.Operator):
    """Function list for current button"""
    bl_idname = "pybtnbox.editor_btn_funclist_current"
    bl_label = "Button Functions"
    
    button_path : bpy.props.StringProperty(default="")
    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_popup(self)
    
    def draw(self, context):
        layout = self.layout
        layout.label(text = 'Current Button')
        layout.operator( 'text.open' ,text='Load To Text Editor',icon= "APPEND_BLEND"  ).filepath  = self.button_path
        layout.operator( "pybtnbox.editor_btn_del" ,text='Remove',icon= "TRASH"  ).filepath  = self.button_path
        
# Button Delete
class PYBTNBOX_OT_Editor_Btn_Del(bpy.types.Operator):
    """Delete This Button"""
    bl_idname = "pybtnbox.editor_btn_del"
    bl_label = "Remove Btn"
    filepath : bpy.props.StringProperty(default="")

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
    def execute(self, context):
        Editor = context.scene.pybtnbox_prop_editor
        Menu = PyBtnBox.Menu.from_menu_name(Editor.menu) 
        try:
            os.remove(self.filepath)
        except FileNotFoundError:
            self.report({'ERROR'},f'File path is not exist : {self.filepath}')
        Menu.data_update()
        Editor.btn_get=''
        return {'FINISHED'}
    
    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row.alignment='CENTER'
        row.label(text ='Are You Sure To Delete The Button?',icon="TRASH")


# [ UI Btn ]
# Add New
class PYBTNBOX_OT_Editor_Layout_New(bpy.types.Operator):
    """Add A New Layout Item"""
    bl_idname = "pybtnbox.editor_layout_add"
    bl_label = "Add A New Layout Item"

    def execute(self, context):
        Editor = context.scene.pybtnbox_prop_editor
        Menu = PyBtnBox.Menu.from_menu_name(Editor.menu)
        Data = Menu.json
        Keys = Data.keys()
        num = 0

        item_name = f'{num}.ui_layout'
        while item_name in Keys:
            num+=1
            item_name = f'{num}.ui_layout'
        Data[item_name] = {
                'is_ui':True,
                'type':0,
                'icon':"BLANK1",
                'text':'',
        }
        # output json
        import json
        json_data = json.dumps(Data, indent=4)
        with open( Menu.json_path , 'w+') as f:
            f.write(json_data)
        Menu.data_update()
        return {'FINISHED'}

# Delete
class PYBTNBOX_OT_Editor_Layout_Del(bpy.types.Operator):
    """Delete This Button"""
    bl_idname = "pybtnbox.editor_layout_del"
    bl_label = "Remove The Layout Item"
    btn_name : bpy.props.StringProperty(default="")

    def execute(self, context):
        Editor = context.scene.pybtnbox_prop_editor
        Menu = PyBtnBox.Menu.from_menu_name(Editor.menu) 
        Data = Menu.json
        if self.btn_name in Data :
            del Data[self.btn_name]
        Menu.data_update()
        Editor.btn_get=''
        return {'FINISHED'}


""""""""" Register """""""""
class_list=[
    # [System]
    PYBTNBOX_OT_ReloadData,
    PYBTNBOX_OT_Menu_Open_Folder,
    # [Menu]
    PYBTNBOX_OT_Btn_Execute,
    PYBTNBOX_OT_Btn_Description,
    
    # [Editor]
    # Menu
    PYBTNBOX_OT_Editor_Menu_Update,
    PYBTNBOX_OT_Editor_Menu_Function_List_Current,
    PYBTNBOX_OT_Editor_Menu_New,
    PYBTNBOX_OT_Editor_Menu_Del,
    # Button
    PYBTNBOX_OT_Editor_Btn_Get,
    PYBTNBOX_OT_Editor_Btn_Get_Cancel,

    PYBTNBOX_OT_Editor_Btn_Update,
    PYBTNBOX_OT_Editor_Btn_OrderWalk,
    PYBTNBOX_OT_Editor_Btn_Function_List_Add,
    PYBTNBOX_OT_Editor_Btn_New,
    
    PYBTNBOX_OT_Editor_Btn_Function_List_Current,
    PYBTNBOX_OT_Editor_Btn_LoadToTextEditor,
    PYBTNBOX_OT_Editor_Btn_Del,
    # [UI Btn]
    PYBTNBOX_OT_Editor_Layout_New,
    PYBTNBOX_OT_Editor_Layout_Del
    ]    

def register():
    for cls in class_list:
        bpy.utils.register_class(cls)



def unregister():
    for cls in class_list:
        bpy.utils.unregister_class(cls)

