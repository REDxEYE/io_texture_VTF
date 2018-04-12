
# from ctypes import c_ubyte,c_float
# from PIL import Image
import numpy as np
import sys

try:
    import bpy
except:
    pass
try:
    from ValveFileSystem.path import Path
    from VTFWrapper import VTFLib
    from VTFWrapper import VTFLibEnums
except:
    from .ValveFileSystem.path import Path
    from .VTFWrapper import VTFLib
    from .VTFWrapper import VTFLibEnums
    import bpy
vtf_lib = VTFLib.VTFLib()
class VTF:

    def __init__(self,filepath):
        self.filepath = Path(filepath).abs()
        self.filename = self.filepath.name(True)
        
    def load(self):
        print('Loading {}'.format(self.filepath.name(True)))
        vtf_lib.image_load(self.filepath)
        if vtf_lib.image_is_loaded():
            print('Image loaded successfully')
            pass
        else:
            raise Exception("Failed to load texture :{}".format(vtf_lib.get_last_error()))

    def read_image(self):
        rgba_data = vtf_lib.convert_to_rgba8888()
        rgba_data = vtf_lib.flip_image(rgba_data)
        try:
            image = bpy.data.images.new(self.filename, width=vtf_lib.width(), height=vtf_lib.height())
            image.pixels = np.divide(rgba_data.contents,255.0)
            image.pack(as_png=True)
            return image
        except Exception as ex:
            print(ex)
            return None



if __name__ == '__main__':
    vtf = VTF(r'E:\PYTHON_STUFF\SourceVTF\test_data\DeathClaw_D.vtf')
    vtf.load()
    vtf.read_image()