import bpy
import json
import importlib.util
import os

bl_info = {
"name" : "PyBtnBox",
"author" : "Ou Chiang",
"version": (1, 0),
"location": "View3D > PyBtnBox",
"description" : "Python Button Box",
"category" : "3D View"
}



""""""""" Paths """""""""
class Path:
    root = os.path.dirname( os.path.abspath(__file__) )
    pyFolders = root + '\\pyFolders\\'
    preset = root + '\\preset.json'

    @classmethod
    def pyFolder(self,folderName):
        return self.root + '\\pyFolders\\'+ folderName
    @classmethod
    def menuData(self,folderName):
        return self.root + '\\pyFolders\\'+ folderName + '\\_menuData.json'
    @classmethod
    def pyFile(self,folderName,pyName):
        return self.pyFolder(folderName) + '\\' + pyName + '.py'
    
    @classmethod
    def btnIcon(self,folderName,picName,picType):
         picPath = self.pyFolder(folderName) + '\\' + picName +'.'+ picType
         return picPath
    

""""""""" Lists """""""""
class List:
    pyFolders =[ d for d in os.listdir( Path.pyFolders ) if os.path.isdir( Path.pyFolders + d ) ]
    
    @staticmethod
    def pyFiles(folderNm):
        files = os.listdir( Path.pyFolder(folderNm) )
        return [ d.replace('.py','') for d in files if d.endswith('.py')]
    @staticmethod
    def pictures(folderNm):
        picTypes = ['.png','.jpg']
        files = os.listdir( Path.pyFolder(folderNm) )
        return [ pic for pic in files for typ in picTypes if pic.endswith(typ)]



folders  = List.pyFolders

""""""""" Json """""""""
class Json:
    @staticmethod
    def load(jsonPath):
        with open(jsonPath, 'r') as f:
            return json.load(f)
    
    @staticmethod
    def output(jsonPath,data):
        json_data = json.dumps(data, indent=4)
        with open( jsonPath , 'w+') as f:
            f.write(json_data)



""" rebuild menu """
class PyMenu:
    @staticmethod
    def new( folder ):
        data = {}
        for py in List.pyFiles( folder ) :
            data[ py ] ={}
            data[ py ]['text'] = "function "
            data[ py ]['icon'] = "SCRIPT"
        Json.output( jsonPath , data )
        return data
    @staticmethod
    def reset(jsonPath,folder):
        data = Json.load( jsonPath )
        pys  = List.pyFiles( folder )
        for py in pys:
            if py not in list(data.keys()):
                data[ py ] ={}
                data[ py ]['text'] = "function "
                data[ py ]['icon'] = "SCRIPT"
        for py in list(data.keys()):
            if py not in pys:
                del data[ py ]
        Json.output( jsonPath , data )
        return data
    @staticmethod
    def pyFiles( folderNm ):
        menu = Json.load(Path.menuData( folderNm ))
        return list(menu.keys())
# rebuild menu
#if no PyMenu in folder >> add new json 
#if PyMenu in folder >> reset json
for folder in List.pyFolders:
    jsonPath = Path.menuData( folder )
    if not os.path.isfile( jsonPath ):
        PyMenu.new( folder )
    else :
        PyMenu.reset( jsonPath , folder )


""" Dictionary """
#[get][dict] : {folders : pyfiles}
main_data = {}
for folder in List.pyFolders:
    main_data[folder] = PyMenu.pyFiles( folder )


""" Preset """
# [ add ] : new preset json if preset.json is not exist
#if not os.path.isfile( presetPath ):
if not os.path.isfile( Path.preset ):
    presetData = {'text':False , 'input':False , 'walk':False }
    Json.output( Path.preset , presetData )

# [input] : preset data
Preset = Json.load(Path.preset)

""""""""" Operator """""""""
#[menu][func] : [open][file or folder]
class BB_OT_openFile(bpy.types.Operator):
    bl_idname = "bb.open_file"
    bl_label = "OpenFile"
    Path : bpy.props.StringProperty(default="")
    def execute(self, context):
        os.startfile( self.Path )
        return {'FINISHED'}

#[btn][func] : [run button function]
class BB_OT_pyFunction(bpy.types.Operator):
    bl_idname = "bb.btn_run"
    bl_label = "Button"
    File : bpy.props.StringProperty(default="")
    
    def execute(self, context):
        spec = importlib.util.spec_from_file_location("module.name", self.File )
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
        try:
            foo.main()
        except:
            print('function failed')
        return {'FINISHED'}

#[menu][func] : [ save setting ]
class BB_OT_saveOrder(bpy.types.Operator):
    bl_idname = "bb.save_order"
    bl_label = "Save Button Order"
    Path : bpy.props.StringProperty(default="")
    def execute(self, context):
        # [ save ] : buttons order
        folder = List.pyFolders[ int( bpy.context.scene.bb_menu.BB_Menu ) ]
        j_keys = main_data[ folder ]
        oldData = Json.load( self.Path )

        new_dict = {}
        for f in j_keys:
            new_dict[ f ] = oldData[ f ]
        Json.output( self.Path , new_dict )
        
        # [ save ] : ui preset
        Menu = context.scene.bb_menu
        presetData = {}
        presetData['menu']  = Menu.BB_Menu
        presetData['text']  = Menu.showText
        presetData['input'] = Menu.showInput
        presetData['walk']  = Menu.showOrder
        Json.output( Path.preset , presetData )

        return {'FINISHED'}


#[btn][func] : [walk up] & [walk down]
def j_walk(item,walk):
    folder = List.pyFolders[ int( bpy.context.scene.bb_menu.BB_Menu ) ]
    j_keys = main_data[ folder ]
    Index = j_keys.index( item )
    if   walk =='up':
        if Index-1 >= 0:
            j_keys.remove(item)
            j_keys.insert( Index-1 , item )
    elif walk =='down':
        if Index+1 <= len(j_keys)-1:
            j_keys.remove(item)
            j_keys.insert( Index+1 , item )
    else:
        print('j_walk error')

class BB_OT_up(bpy.types.Operator):
    bl_idname = "bb.btn_up"
    bl_label = "Button Up"
    Item : bpy.props.StringProperty(default="")

    def execute(self, context):
        j_walk(self.Item , 'up')
        return {'FINISHED'}

#[btn] : [walk down]
class BB_OT_down(bpy.types.Operator):
    bl_idname = "bb.btn_down"
    bl_label = "Button Down"
    Item : bpy.props.StringProperty(default="")
    def execute(self, context):
        j_walk(self.Item , 'down')
        return {'FINISHED'}

""""""""" Menu """""""""
def menu_items():
    items = []
    for i in  range(len( List.pyFolders )):
        item = ( str(i) , List.pyFolders[i] , '')
        items.append(item)
    return items

class BB_Menu(bpy.types.PropertyGroup):
    BB_Menu : bpy.props.EnumProperty(
        name="Menu",
        description="Menus where the python file in",
        items = menu_items(),
        default=Preset['menu']
        )
    showText  : bpy.props.BoolProperty(
        name="show text",
        description="Show buttons detail",
        default = Preset['text']
        )
    showOrder : bpy.props.BoolProperty(
        name="show walk button",
        description="Show upWalk and downWalk buttons",
        default = Preset['walk']
        )
    showInput : bpy.props.BoolProperty(
        name="show input script button",
        description="Show input script button",
        default = Preset['input']
        )
""""""""" Panel """""""""
#[panel] : [Button Box Panel]
class BB_PT_mainPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Py Button Panel"
    bl_idname = "BB_PT"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "pyBtnBox"

    def draw_header(self, context):
        self.layout.label(text = "", icon = "SCRIPT")

    def draw(self, context):

        layout = self.layout
        Menu = context.scene.bb_menu
        try : folder = List.pyFolders[ int(Menu.BB_Menu) ]
        except : folder = List.pyFolders[0]
        #folderPath = Path.pyFolder( folder )
        jsPath = Path.menuData( folder )
        
        row = layout.row()
        row.operator("script.reload",text='',icon='FILE_REFRESH')
        row.operator( BB_OT_openFile.bl_idname  ,text='MenuData'  ,icon= "TEXT"      ).Path = Path.menuData( folder )
        row.operator( BB_OT_openFile.bl_idname  ,text='PyFolder'  ,icon='FILEBROWSER').Path = Path.pyFolder( folder )
        row.operator( BB_OT_saveOrder.bl_idname ,text='SaveSetting',icon='FILE_TICK' ).Path = Path.menuData( folder )

        row = layout.row()
        row.prop(Menu, "BB_Menu")

        row = layout.row()
        row.label( text = "Layout :")
        row.prop(Menu, "showText", text="Text")
        row.prop(Menu, "showInput", text="Input")
        row.prop(Menu, "showOrder", text="Order")
        
        menuData = Json.load( jsPath )
        pyBtns = main_data[ folder ]

        def btns_xT_xI_xW():
            box = layout.box()
            box_row = box.row(align = True)
            box_row.label( icon = menuData[ pyBtns[i] ]['icon'] )
            box_row.operator(BB_OT_pyFunction.bl_idname ,text= pyBtns[i]).File = Path.pyFile(folder,pyBtns[i])
        
        def btns_xT_xI_oW():
            box = layout.box()
            box_row = box.row(align = True)
            box_row.label( icon = menuData[ pyBtns[i] ]['icon'] )
            box_row.operator(BB_OT_pyFunction.bl_idname ,text= pyBtns[i]).File = Path.pyFile(folder,pyBtns[i])
            box_row.operator( BB_OT_up.bl_idname   ,text='',icon= "TRIA_UP"   ).Item  = pyBtns[i]
            box_row.operator( BB_OT_down.bl_idname ,text='',icon= "TRIA_DOWN" ).Item  = pyBtns[i]
        
        def btns_xT_oI_xW():
            box = layout.box()
            box_row = box.row(align = True)
            box_row.label( icon = menuData[ pyBtns[i] ]['icon'] )
            box_row.operator(BB_OT_pyFunction.bl_idname ,text= pyBtns[i]).File = Path.pyFile(folder,pyBtns[i])
            box_row.operator( 'text.open'   ,text='',icon= "TEXT"  ).filepath  = Path.pyFile(folder,pyBtns[i])
        
        def btns_xT_oI_oW():
            box = layout.box()
            box_row = box.row(align = True)
            box_row.label( icon = menuData[ pyBtns[i] ]['icon'] )
            box_row.operator(BB_OT_pyFunction.bl_idname ,text= pyBtns[i]).File = Path.pyFile(folder,pyBtns[i])
            box_row.operator( 'text.open'   ,text='',icon= "TEXT"  ).filepath  = Path.pyFile(folder,pyBtns[i])
            box_row.operator( BB_OT_up.bl_idname   ,text='',icon= "TRIA_UP"   ).Item  = pyBtns[i]
            box_row.operator( BB_OT_down.bl_idname ,text='',icon= "TRIA_DOWN" ).Item  = pyBtns[i]
        
        def btns_oT_xI_xW():
            box = layout.box()
            box_row = box.row(align = True)
            split = box_row.split(factor = 0.7,align = True)
            split.label( icon = menuData[ pyBtns[i] ]['icon'] ,text = menuData[ pyBtns[i] ]['text'] )
            split.operator(BB_OT_pyFunction.bl_idname ,text= pyBtns[i]).File = Path.pyFile(folder,pyBtns[i])
        
        def btns_oT_xI_oW():
            box = layout.box()
            box_row = box.row(align = True)
            split = box_row.split(factor = 0.7,align = True)
            split.label( icon = menuData[ pyBtns[i] ]['icon'] ,text = menuData[ pyBtns[i] ]['text'] )
            split.operator(BB_OT_pyFunction.bl_idname ,text= pyBtns[i]).File = Path.pyFile(folder,pyBtns[i])
            box_row.operator( BB_OT_up.bl_idname   ,text='',icon= "TRIA_UP"   ).Item  = pyBtns[i]
            box_row.operator( BB_OT_down.bl_idname ,text='',icon= "TRIA_DOWN" ).Item  = pyBtns[i]
        
        def btns_oT_oI_xW():
            box = layout.box()
            box_row = box.row(align = True)
            split = box_row.split(factor = 0.7,align = True)
            split.label( icon = menuData[ pyBtns[i] ]['icon'] ,text = menuData[ pyBtns[i] ]['text'] )
            split.operator(BB_OT_pyFunction.bl_idname ,text= pyBtns[i]).File = Path.pyFile(folder,pyBtns[i])
            box_row.operator( 'text.open'   ,text='',icon= "TEXT"  ).filepath  = Path.pyFile(folder,pyBtns[i])
        
        def btns_oT_oI_oW():
            box = layout.box()
            box_row = box.row(align = True)
            split = box_row.split(factor = 0.7,align = True)
            split.label( icon = menuData[ pyBtns[i] ]['icon'] ,text = menuData[ pyBtns[i] ]['text'] )
            split.operator(BB_OT_pyFunction.bl_idname ,text= pyBtns[i]).File = Path.pyFile(folder,pyBtns[i])
            box_row.operator( 'text.open'   ,text='',icon= "TEXT"  ).filepath  = Path.pyFile(folder,pyBtns[i])
            box_row.operator( BB_OT_up.bl_idname   ,text='',icon= "TRIA_UP"   ).Item  = pyBtns[i]
            box_row.operator( BB_OT_down.bl_idname ,text='',icon= "TRIA_DOWN" ).Item  = pyBtns[i]

        #[btn] : [show] [btns] by menu item
        show_select = 'btns'
        if Menu.showText == True:show_select += '_oT'
        else:show_select += '_xT'

        if Menu.showInput == True:show_select += '_oI'
        else:show_select += '_xI'

        if Menu.showOrder == True:show_select += '_oW'
        else:show_select += '_xW'
        
        show_select += '()'
        for i in range(len(pyBtns)) :
            exec(show_select)

""""""""" Register """""""""
class_list = [
    BB_PT_mainPanel,
    BB_OT_openFile,
    BB_OT_pyFunction,
    BB_OT_saveOrder,
    BB_OT_up,
    BB_OT_down
]




def register():
    bpy.utils.register_class(BB_Menu)
    bpy.types.Scene.bb_menu = bpy.props.PointerProperty(type=BB_Menu)

    for Class in class_list:
        bpy.utils.register_class(Class)
    print('register')


def unregister():
    bpy.utils.unregister_class(BB_Menu)
    del bpy.types.Scene.bb_menu
    for Class in class_list:
        bpy.utils.unregister_class(Class)
    print('unregister')
