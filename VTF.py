# from ctypes import c_ubyte,c_float
# from PIL import Image
from ctypes import create_string_buffer
from pathlib import Path

import numpy as np

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


def import_texture(path, load_alpha=True, alpha_only=False):
    path = Path(path).absolute()
    name = path.stem
    print('Loading {}'.format(name))
    vtf_lib.image_load(str(path))
    if vtf_lib.image_is_loaded():
        print('Image loaded successfully')
        pass
    else:
        raise Exception("Failed to load texture :{}".format(vtf_lib.get_last_error()))
    rgba_data = vtf_lib.convert_to_rgba8888()
    print('Converted')
    rgba_data = vtf_lib.flip_image_external(rgba_data, vtf_lib.width(), vtf_lib.height())
    print('Flipped')
    pixels = np.array(rgba_data.contents, np.uint8)
    pixels = pixels.astype(np.float16, copy=False)
    has_alpha = False
    if (vtf_lib.get_image_flags().get_flag(ImageFlag.ImageFlagEightBitAlpha) or vtf_lib.get_image_flags().get_flag(
            ImageFlag.ImageFlagOneBitAlpha)) and load_alpha:
        print('Image has alpha channel, splitting and saving it!')
        alpha_view = pixels[3::4]
        has_alpha = alpha_view.any()
        if load_alpha and has_alpha:
            alpha = alpha_view.copy()
            alpha = np.repeat(alpha, 4)
            alpha[3::4][:] = 255
            if has_alpha:
                print('Saving alpha')
                try:
                    alpha_im = bpy.data.images.new(name + '_A', width=vtf_lib.width(), height=vtf_lib.height())
                    alpha = np.divide(alpha, 255)
                    alpha_im.pixels = alpha
                    alpha_im.pack(as_png=True)
                except Exception as ex:
                    print('Caught exception "{}" '.format(ex))
        alpha_view[:] = 255
        print('Done')
    if not alpha_only:
        print('Saving main texture')
        try:
            image = bpy.data.images.new(name + '_RGB', width=vtf_lib.width(), height=vtf_lib.height())
            pixels = np.divide(pixels, 255)
            image.pixels = pixels
            image.pack(as_png=True)
            return image
        except Exception as ex:
            print('Caught exception "{}" '.format(ex))
    vtf_lib.image_destroy()

    return name + '_RGB',(name + '_A') if has_alpha else None


def export_texture(blender_texture, path):
    image_data = np.array(blender_texture.pixels, np.float16) * 255
    image_data = image_data.astype(np.uint8, copy=False)
    def_options = vtf_lib.create_default_params_structure()
    def_options.ImageFormat = VTFLibEnums.ImageFormat.ImageFormatRGBA8888
    def_options.Flags |= VTFLibEnums.ImageFlag.ImageFlagEightBitAlpha
    def_options.Resize = 1
    w, h = blender_texture.size
    image_data = create_string_buffer(image_data.tobytes())
    image_data = vtf_lib.flip_image_external(image_data, w, h)
    vtf_lib.image_create_single(w, h, image_data, def_options)
    vtf_lib.image_save(path)
    vtf_lib.image_destroy()


if __name__ == '__main__':
    import_texture(r'E:\PYTHON_STUFF\SourceVTF\test_data\brooch_bird_diffuse.vtf')
    # import_texture(r'E:\PYTHON_STUFF\SourceVTF\test_data\alpha.vtf')
