

bl_info = {
    "name": "Source Engine VTF Texture import",
    "author": "RED_EYE",
    "version": (1, 0,),
    "blender": (2, 78, 0),
    'warning': 'Uses a lot of ram (1Gb for 4k texture)',
    "location": "File > Import-Export > Source Engine texture import (VTF)",
    "description": "Import-Export Source Engine texture import (VTF)",
    #"wiki_url": "http://www.barneyparker.com/blender-json-import-export-plugin",
    #"tracker_url": "http://www.barneyparker.com/blender-json-import-export-plugin",
    "category": "Import-Export"}
from . import VTF
# from . import VMT
# from . import BlenderMaterial

import bpy

from bpy.props import StringProperty, BoolProperty
from bpy_extras.io_utils import ExportHelper

import os.path
import sys
print('Appending "{}" to PATH'.format(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

class VTFImporter(bpy.types.Operator):
    """Load Source Engine VTF texture"""
    bl_idname = "import_texture.vtf"
    bl_label = "Import VTF"
    bl_options = {'UNDO'}

    filepath = StringProperty(
            subtype='FILE_PATH',
            )
    load_alpha = BoolProperty(default=False, name='Load alpha')
    only_alpha = BoolProperty(default=False, name='Only load alpha')
    filter_glob = StringProperty(default="*.vtf", options={'HIDDEN'})

    def execute(self, context):
        VTF.import_texture(self.filepath,self.load_alpha,self.only_alpha)
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        wm.fileselect_add(self)
        return {'RUNNING_MODAL'}

# class VMTImporter(bpy.types.Operator):
#     """Load Source Engine VMT material"""
#     bl_idname = "import_texture.vmt"
#     bl_label = "Import VMT"
#     bl_options = {'UNDO'}
#
#     filepath = StringProperty(
#             subtype='FILE_PATH',
#             )
#
#     filter_glob = StringProperty(default="*.vmt", options={'HIDDEN'})
#     game = StringProperty(name="PATH TO GAME",subtype='FILE_PATH',default = "" )
#     override = BoolProperty(default = False,name='Override existing?')
#
#     def execute(self, context):
#         vmt = VMT.VMT(self.filepath,self.game)
#         mat = BlenderMaterial.BlenderMaterial(vmt)
#         mat.load_textures()
#         if mat.create_material(self.override) == 'EXISTS' and not self.override:
#             self.report({'INFO'},'{} material already exists')
#         return {'FINISHED'}
#
#     def invoke(self, context, event):
#         wm = context.window_manager
#         wm.fileselect_add(self)
#         return {'RUNNING_MODAL'}
class VTFExport(bpy.types.Operator):
    """Export VTF texture"""
    bl_idname = "export_texture.vtf"
    bl_label = "Export VTF"
    bl_options = {'UNDO'}

    filepath = StringProperty(
            subtype='FILE_PATH',
            )

    filter_glob = StringProperty(default="*.vtf", options={'HIDDEN'})

    def execute(self, context):
        sima = context.space_data
        ima = sima.image
        print(context)
        VTF.export_texture(ima,self.filepath)
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        wm.fileselect_add(self)
        return {'RUNNING_MODAL'}


def menu_import(self, context):
    self.layout.operator(VTFImporter.bl_idname, text="VTF texture (.vtf)")
    # self.layout.operator(VMTImporter.bl_idname, text="VMT texture (.vmt)")

def export(self,context):
    self.layout.operator(VTFExport.bl_idname,text='Export to VTF')

def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_file_import.append(menu_import)
    bpy.types.IMAGE_MT_image.append(export)


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_file_import.remove(menu_import)


if __name__ == "__main__":
    register()
