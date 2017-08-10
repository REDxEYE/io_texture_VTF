bl_info = {
    "name": "Source Engine VTF Texture import",
    "author": "RED_EYE",
    "version": (0, 6),
    "blender": (2, 78, 0),
    "location": "File > Import-Export > Source Engine texture import (VTF)",
    "description": "Import-Export Source Engine texture import (VTF)",
    "warning": "",
    #"wiki_url": "http://www.barneyparker.com/blender-json-import-export-plugin",
    #"tracker_url": "http://www.barneyparker.com/blender-json-import-export-plugin",
    "category": "Import-Export"}
from . import VTF

import bpy

from bpy.props import StringProperty, BoolProperty
from bpy_extras.io_utils import ExportHelper



class VTFImporter(bpy.types.Operator):
    """Load Source Engine VTF texture"""
    bl_idname = "import_texture.vtf"
    bl_label = "Import VTF"
    bl_options = {'UNDO'}

    filepath = StringProperty(
            subtype='FILE_PATH',
            )

    filter_glob = StringProperty(default="*.vtf", options={'HIDDEN'})

    def execute(self, context):
        VTF.VTF(self.filepath)
        try:
            bpy.ops.import_texture.vtf
        except:
            self.report({'WARNING'},"IO_TEXTURE_VTF NOT INSTALLED!")
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        wm.fileselect_add(self)
        return {'RUNNING_MODAL'}


def menu_import(self, context):
    self.layout.operator(VTFImporter.bl_idname, text="VTF texture (.vtf)")

def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_file_import.append(menu_import)


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_file_import.remove(menu_import)


if __name__ == "__main__":
    register()
