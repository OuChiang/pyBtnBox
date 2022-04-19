import bpy
import os

Dir = os.path.dirname(os.path.abspath(__file__))
File = 'AppendData.blend'
Inner = 'Material'
Material = 'test_material'

filepath = os.path.join(Dir,File, Inner, Material)
directory= os.path.join(Dir,File, Inner)
 
bpy.ops.wm.append(filepath=filepath,directory=directory,filename=Material)