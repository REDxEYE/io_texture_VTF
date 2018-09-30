# from ctypes import c_ubyte,c_float
# from PIL import Image
import numpy as np
from pathlib import Path


try:
    import bpy
except:
    pass
try:
    from VTFWrapper.VTFLibEnums import ImageFlag
    from VTFWrapper import VTFLib
    from VTFWrapper import VTFLibEnums
except:
    from .VTFWrapper.VTFLibEnums import ImageFlag
    from .VTFWrapper import VTFLib
    from .VTFWrapper import VTFLibEnums
    import bpy
vtf_lib = VTFLib.VTFLib()


class VTF:

    def __init__(self, filepath):
        self.filepath = Path(filepath).absolute()
        self.filename = self.filepath.stem
        self.has_alpha = False

    def load(self):
        print('Loading {}'.format(self.filepath.stem))
        vtf_lib.image_load(str(self.filepath))
        if vtf_lib.image_is_loaded():
            print('Image loaded successfully')
            pass
        else:
            raise Exception("Failed to load texture :{}".format(vtf_lib.get_last_error()))

    def read_image(self):
        print('Converting to RGBA8888')
        rgba_data = vtf_lib.convert_to_rgba8888()
        rgba_data = vtf_lib.flip_image(rgba_data)
        pixels = np.divide(rgba_data.contents, 255.0)
        alpha = []
        if vtf_lib.get_image_flags().get_flag(ImageFlag.ImageFlagEightBitAlpha) or vtf_lib.get_image_flags().get_flag(ImageFlag.ImageFlagOneBitAlpha):
            self.has_alpha = True
            print('Image has alpha channel, splitting and removing it!')
            alpha_view = pixels[3::4]
            alpha = alpha_view.copy()
            alpha_view[:]=255
            alpha = np.repeat(alpha, 4)
            alpha[3::4] = 255
            print('Done')
        print('Saving new textures')
        try:
            image = bpy.data.images.new(self.filename+'_RGB', width=vtf_lib.width(), height=vtf_lib.height())
            image.pixels = pixels
            image.pack(as_png=True)
        except Exception as ex:
            print('Caught exception "{}" '.format(ex))
        if self.has_alpha:
            print('Saving alpha')
            try:
                alpha_im = bpy.data.images.new(self.filename + '_A', width=vtf_lib.width(), height=vtf_lib.height())
                alpha_im.pixels = alpha
                alpha_im.pack(as_png=True)
            except Exception as ex:
                print('Caught exception "{}" '.format(ex))

def export_texture(blender_texture,path):
    image_data = np.array(blender_texture.pixels,np.float)
    image_data = np.asarray(image_data*256,np.uint8)
    def_options = vtf_lib.image_create_default_create_structure()
    def_options.ImageFormat = VTFLibEnums.ImageFormat.ImageFormatRGBA8888
    def_options.Flags |= VTFLibEnums.ImageFlag.ImageFlagEightBitAlpha
    w,h = blender_texture.size
    vtf_lib.image_create_single(w, h, image_data.tobytes(), def_options)
    vtf_lib.image_save(path)


if __name__ == '__main__':
    vtf = VTF(r'E:\PYTHON_STUFF\SourceVTF\test_data\DeathClaw_D.vtf')
    vtf.load()
    print(vtf_lib.get_image_flags())
    vtf.read_image()
