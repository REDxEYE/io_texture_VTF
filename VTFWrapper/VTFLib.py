import os
import platform
import sys
from ctypes import *



try:
    from VTFWrapper.VTFLibEnums import ImageFlag
    import VTFLibEnums, VTFLibConstants, VTFLibStructures
except:
    from .VTFLibEnums import ImageFlag
    from . import VTFLibEnums, VTFLibStructures, VTFLibConstants
isWin64 = platform.architecture(executable=sys.executable, bits='', linkage='')[0] == "64bit"
_vtf_lib = "VTFLib.x64.dll" if isWin64 else "VTFLib.x86.dll"
full_path = os.path.dirname(__file__)


# print(full_path)
class VTFLib:
    # print(_vtf_lib)
    dll = WinDLL(os.path.join(full_path, _vtf_lib))

    def __init__(self):
        self.initialize()
        self.image_buffer = c_int()
        self.create_image(byref(self.image_buffer))
        self.bind_image(self.image_buffer)

    def pointer_to_array(self, poiter, size, type=c_ubyte):
        return cast(poiter, POINTER(type * size))

    GetVersion = dll.vlGetVersion
    GetVersion.argtypes = []
    GetVersion.restype = c_uint32

    def get_version(self):
        return self.GetVersion()

    Initialize = dll.vlInitialize
    Initialize.argtypes = []
    Initialize.restype = c_bool

    def initialize(self):
        return self.Initialize()

    Shutdown = dll.vlShutdown
    Shutdown.argtypes = []
    Shutdown.restype = c_bool

    def shutdown(self):
        return self.Shutdown()

    GetVersionString = dll.vlGetVersionString
    GetVersionString.argtypes = []
    GetVersionString.restype = c_char_p

    def get_str_version(self):
        return self.GetVersionString().decode('utf')

    GetLastError = dll.vlGetLastError
    GetLastError.argtypes = []
    GetLastError.restype = c_char_p

    def get_last_error(self):
        bytes().decode()
        error = self.GetLastError().decode('utf', "replace")
        return error if error else "No errors"

    GetBoolean = dll.vlGetBoolean
    GetBoolean.argtypes = [VTFLibEnums.Option]
    GetBoolean.restype = c_bool

    def get_boolean(self, option):
        return self.GetBoolean(option)

    SetBoolean = dll.vlSetBoolean
    SetBoolean.argtypes = [VTFLibEnums.Option, c_bool]
    SetBoolean.restype = None

    def set_boolean(self, option, value):
        self.SetBoolean(option, value)

    GetInteger = dll.vlGetInteger
    GetInteger.argtypes = [c_int32]
    GetInteger.restype = c_int32

    def get_integer(self, option):
        return self.GetInteger(option)

    SetInteger = dll.vlSetInteger
    SetInteger.argtypes = [VTFLibEnums.Option, c_int32]
    SetInteger.restype = None

    def set_integer(self, option, value):
        self.SetInteger(option, value)

    GetFloat = dll.vlGetFloat
    GetFloat.argtypes = [c_int32]
    GetFloat.restype = c_float

    def get_float(self, option):
        return self.GetFloat(option)

    SetFloat = dll.vlSetFloat
    SetFloat.argtypes = [VTFLibEnums.Option, c_float]
    SetFloat.restype = None

    def set_float(self, option, value):
        self.SetFloat(option, value)

    ImageIsBound = dll.vlImageIsBound
    ImageIsBound.argtypes = []
    ImageIsBound.restype = c_bool

    def image_is_bound(self):
        return self.ImageIsBound()

    BindImage = dll.vlBindImage
    BindImage.argtypes = [c_int32]
    BindImage.restype = c_bool

    def bind_image(self, image):
        return self.BindImage(image)

    CreateImage = dll.vlCreateImage
    CreateImage.argtypes = [POINTER(c_int)]
    CreateImage.restype = c_bool

    def create_image(self, image):
        return self.CreateImage(image)

    DeleteImage = dll.vlDeleteImage
    DeleteImage.argtypes = [POINTER(c_int32)]
    DeleteImage.restype = None

    def delete_image(self, image):
        self.DeleteImage(image)

    ImageCreateDefaultCreateStructure = dll.vlImageCreateDefaultCreateStructure
    ImageCreateDefaultCreateStructure.argtypes = [POINTER(VTFLibStructures.CreateOptions)]
    ImageCreateDefaultCreateStructure.restype = None

    def image_create_default_create_structure(self, create_oprions):
        self.ImageCreateDefaultCreateStructure(pointer(create_oprions))
        return create_oprions

    ImageCreate = dll.vlImageCreate
    ImageCreate.argtypes = [c_int32, c_int32, c_int32, c_int32, c_int32, VTFLibEnums.ImageFormat, c_bool, c_bool,
                            c_bool]
    ImageCreate.restype = c_byte

    def image_create(self, width, height, frames, faces, slices, image_format, thumbnail, mipmaps, nulldata):
        return self.ImageCreate(width, height, frames, faces, slices, image_format, thumbnail, mipmaps, nulldata)

    ImageDestroy = dll.vlImageDestroy
    ImageDestroy.argtypes = []
    ImageDestroy.restype = None

    def image_destroy(self):
        self.ImageDestroy()

    ImageIsLoaded = dll.vlImageIsLoaded
    ImageIsLoaded.argtypes = []
    ImageIsLoaded.restype = c_bool

    def image_is_loaded(self):
        return self.ImageIsLoaded()

    ImageLoad = dll.vlImageLoad
    ImageLoad.argtypes = [c_char_p, c_bool]
    ImageLoad.restype = c_bool

    def image_load(self, filename, header_only=False):
        # str_buff = cast(filename,c_char_p)
        # print(str_buff.value)
        return self.ImageLoad(create_string_buffer(filename.encode('ascii')), header_only)

    ImageSave = dll.vlImageSave
    ImageSave.argtypes = [c_char_p]
    ImageSave.restype = c_bool

    def image_save(self, filename):
        return self.ImageSave(create_string_buffer(filename.encode('ascii')))

    ImageGetSize = dll.vlImageGetSize
    ImageGetSize.argtypes = []
    ImageGetSize.restype = c_int32

    def get_size(self):
        return self.ImageGetSize()

    ImageGetWidth = dll.vlImageGetWidth
    ImageGetWidth.argtypes = []
    ImageGetWidth.restype = c_int32

    def width(self):
        return self.ImageGetWidth()

    ImageGetHeight = dll.vlImageGetHeight
    ImageGetHeight.argtypes = []
    ImageGetHeight.restype = c_int32

    def height(self):
        return self.ImageGetHeight()

    ImageGetDepth = dll.vlImageGetDepth
    ImageGetDepth.argtypes = []
    ImageGetDepth.restype = c_int32

    def depth(self):
        return self.ImageGetDepth()

    ImageGetFrameCount = dll.vlImageGetFrameCount
    ImageGetFrameCount.argtypes = []
    ImageGetFrameCount.restype = c_int32

    def frame_count(self):
        return self.ImageGetFrameCount()

    ImageGetFaceCount = dll.vlImageGetFaceCount
    ImageGetFaceCount.argtypes = []
    ImageGetFaceCount.restype = c_int32

    def face_count(self):
        return self.ImageGetFaceCount()

    ImageGetMipmapCount = dll.vlImageGetMipmapCount
    ImageGetMipmapCount.argtypes = []
    ImageGetMipmapCount.restype = c_int32

    def mipmap_count(self):
        return self.ImageGetMipmapCount()

    ImageGetStartFrame = dll.vlImageGetStartFrame
    ImageGetStartFrame.argtypes = []
    ImageGetStartFrame.restype = c_int32

    def get_start_frame(self):
        return self.ImageGetStartFrame()

    ImageSetStartFrame = dll.vlImageSetStartFrame
    ImageSetStartFrame.argtypes = [c_int32]
    ImageSetStartFrame.restype = None

    def set_start_frame(self, start_frame):
        return self.ImageSetStartFrame(start_frame)

    ImageGetFlags = dll.vlImageGetFlags
    ImageGetFlags.argtypes = []
    ImageGetFlags.restype = c_int32

    def get_image_flags(self):
        return ImageFlag(self.ImageGetFlags())

    ImageSetFlags = dll.vlImageSetFlags
    ImageSetFlags.argtypes = [c_float]
    ImageSetFlags.restype = None

    def set_image_flags(self, flags):
        return self.ImageSetFlags(flags)

    ImageGetFormat = dll.vlImageGetFormat
    ImageGetFormat.argtypes = []
    ImageGetFormat.restype = VTFLibEnums.ImageFormat

    def image_format(self):
        return self.ImageGetFormat()

    ImageGetData = dll.vlImageGetData
    ImageGetData.argtypes = [c_uint32, c_uint32, c_uint32, c_uint32]
    ImageGetData.restype = POINTER(c_byte)

    def get_image_data(self, frame=0, face=0, slice=0, mipmap_level=0):
        size = self.compute_image_size(self.width(), self.height(), self.depth(), self.mipmap_count(),
                                       self.image_format().value)
        buff = self.ImageGetData(frame, face, slice, mipmap_level)
        return self.pointer_to_array(buff, size)

    def get_rgba8888(self):
        size = self.compute_image_size(self.width(), self.height(), self.depth(), self.mipmap_count(),
                                       VTFLibEnums.ImageFormat.ImageFormatRGBA8888)
        if self.image_format() == VTFLibEnums.ImageFormat.ImageFormatRGBA8888:
            return self.pointer_to_array(self.get_image_data(0, 0, 0, 0), size)

        return self.pointer_to_array(self.convert_to_rgba8888(), size)

    def get_as_float(self):
        new_size = self.compute_image_size(self.width(), self.height(), self.depth(), self.mipmap_count(),
                                           VTFLibEnums.ImageFormat.ImageFormatRGBA16161616)
        new_buffer = cast((c_byte * new_size)(), POINTER(c_byte))
        if not self.ImageConvert(self.ImageGetData(0, 0, 0, 0), new_buffer, self.width(), self.height(),
                                 self.image_format().value, VTFLibEnums.ImageFormat.ImageFormatRGBA16161616):
            return self.pointer_to_array(new_buffer, new_size, c_ubyte).contents
        else:
            sys.stderr.write('CAN\'T CONVERT IMAGE\n')
            return 0

    ImageSetData = dll.vlImageSetData
    ImageSetData.argtypes = [c_uint32, c_uint32, c_uint32, c_uint32, POINTER(c_byte)]
    ImageSetData.restype = None

    def set_image_data(self, frame, face, slice, mipmap_level, data):
        return self.ImageSetData(frame, face, slice, mipmap_level, data)

    ImageGetHasThumbnail = dll.vlImageGetHasThumbnail
    ImageGetHasThumbnail.argtypes = []
    ImageGetHasThumbnail.restype = c_bool

    def has_thumbnail(self):
        return self.ImageGetHasThumbnail()

    ImageGetThumbnailWidth = dll.vlImageGetThumbnailWidth
    ImageGetThumbnailWidth.argtypes = []
    ImageGetThumbnailWidth.restype = c_int32

    def thumbnail_width(self):
        return self.ImageGetThumbnailWidth()

    ImageGetThumbnailHeight = dll.vlImageGetThumbnailHeight
    ImageGetThumbnailHeight.argtypes = []
    ImageGetThumbnailHeight.restype = c_int32

    def thumbnail_height(self):
        return self.ImageGetThumbnailHeight()

    ImageGetThumbnailFormat = dll.vlImageGetThumbnailFormat
    ImageGetThumbnailFormat.argtypes = []
    ImageGetThumbnailFormat.restype = VTFLibEnums.ImageFormat

    def thumbnail_format(self):
        return self.ImageGetThumbnailFormat()

    ImageGetThumbnailData = dll.vlImageGetThumbnailData
    ImageGetThumbnailData.argtypes = []
    ImageGetThumbnailData.restype = POINTER(c_byte)

    def get_thumbnail_format_data(self):
        return self.ImageGetThumbnailData()

    ImageSetThumbnailData = dll.vlImageSetThumbnailData
    ImageSetThumbnailData.argtypes = [POINTER(c_byte)]
    ImageSetThumbnailData.restype = None

    def set_thumbnail_format_data(self, data):
        return self.ImageSetThumbnailData(data)

    ImageGenerateMipmaps = dll.vlImageGenerateMipmaps
    ImageGenerateMipmaps.argtypes = [c_uint32, c_uint32, c_uint32, c_uint32]
    ImageGenerateMipmaps.restype = c_bool

    def generate_mipmaps(self, face, frame, mipmap_filter, sharpness_filter):
        return self.ImageGenerateMipmaps(face, frame, mipmap_filter, sharpness_filter)

    ImageGenerateAllMipmaps = dll.vlImageGenerateAllMipmaps
    ImageGenerateAllMipmaps.argtypes = [c_uint32, c_uint32]
    ImageGenerateAllMipmaps.restype = c_bool

    def generate_all_mipmaps(self, mipmap_filter, sharpness_filter):
        return self.ImageGenerateAllMipmaps(mipmap_filter, sharpness_filter)

    ImageGenerateThumbnail = dll.vlImageGenerateThumbnail
    ImageGenerateThumbnail.argtypes = []
    ImageGenerateThumbnail.restype = c_bool

    def generate_thumbnail(self):
        return self.ImageGenerateThumbnail()

    ImageGenerateNormalMap = dll.vlImageGenerateNormalMap
    ImageGenerateNormalMap.argtypes = [c_uint32, c_uint32, c_uint32, c_uint32]
    ImageGenerateNormalMap.restype = c_bool

    def generate_normal_maps(self, frame, kernel_filter, height_conversion_method, normal_alpha_result):
        return self.ImageGenerateNormalMap(frame, kernel_filter, height_conversion_method, normal_alpha_result)

    ImageGenerateAllNormalMaps = dll.vlImageGenerateAllNormalMaps
    ImageGenerateAllNormalMaps.argtypes = [c_uint32, c_uint32, c_uint32, c_uint32]
    ImageGenerateAllNormalMaps.restype = c_bool

    def generate_all_normal_maps(self, kernel_filter, height_conversion_method, normal_alpha_result):
        return self.ImageGenerateAllNormalMaps(kernel_filter, height_conversion_method, normal_alpha_result)

    ImageGenerateSphereMap = dll.vlImageGenerateSphereMap
    ImageGenerateSphereMap.argtypes = []
    ImageGenerateSphereMap.restype = c_bool

    def generate_sphere_map(self):
        return self.ImageGenerateSphereMap()

    ImageComputeReflectivity = dll.vlImageComputeReflectivity
    ImageComputeReflectivity.argtypes = []
    ImageComputeReflectivity.restype = c_bool

    def compute_reflectivity(self):
        return self.ImageComputeReflectivity()

    ImageComputeImageSize = dll.vlImageComputeImageSize
    ImageComputeImageSize.argtypes = [c_int32, c_uint32, c_int32, c_uint32, c_int32]
    ImageComputeImageSize.restype = c_uint32

    def compute_image_size(self, width, height, depth, mipmaps, image_format):
        return self.ImageComputeImageSize(width, height, depth, mipmaps, image_format)

    ImageFlipImage = dll.vlImageFlipImage
    ImageFlipImage.argtypes = [POINTER(c_byte), c_uint32, c_int32]
    ImageFlipImage.restype = None

    def flip_image(self, image_data):
        if self.image_format() != VTFLibEnums.ImageFormat.ImageFormatRGBA8888:
            image_data = self.convert_to_rgba8888()
        image_data = cast(image_data, POINTER(c_byte))
        self.ImageFlipImage(image_data, self.width(), self.height())
        size = self.compute_image_size(self.width(), self.height(), self.depth(), self.mipmap_count(),
                                       VTFLibEnums.ImageFormat.ImageFormatRGBA8888)

        return self.pointer_to_array(image_data, size)

    ImageConvertToRGBA8888 = dll.vlImageConvertToRGBA8888
    ImageConvertToRGBA8888.argtypes = [POINTER(c_byte), POINTER(c_byte), c_uint32, c_int32, c_uint32]
    ImageConvertToRGBA8888.restype = None

    def convert_to_rgba8888(self):
        new_size = self.compute_image_size(self.width(), self.height(), self.depth(), self.mipmap_count(),
                                           VTFLibEnums.ImageFormat.ImageFormatRGBA8888)
        new_buffer = cast((c_byte * new_size)(), POINTER(c_byte))
        # print('Input format:',self.image_format())
        if not self.ImageConvertToRGBA8888(self.ImageGetData(0, 0, 0, 0), new_buffer, self.width(), self.height(),
                                           self.image_format().value):
            return self.pointer_to_array(new_buffer, new_size)
        else:
            sys.stderr.write('CAN\'T CONVERT IMAGE\n')
            return 0

    ImageConvert = dll.vlImageConvert
    ImageConvert.argtypes = [POINTER(c_byte), POINTER(c_byte), c_uint32, c_int32, c_uint32, c_int32]
    ImageConvert.restype = None

    def convert(self, format):
        print("Converting from {} to {}".format(self.image_format().name, VTFLibEnums.ImageFormat(format).name))
        new_size = self.compute_image_size(self.width(), self.height(), self.depth(), self.mipmap_count(), format)
        new_buffer = cast((c_byte * new_size)(), POINTER(c_byte))
        if not self.ImageConvert(self.ImageGetData(0, 0, 0, 0), new_buffer, self.width(), self.height(),
                                 self.image_format().value, format):
            return self.pointer_to_array(new_buffer, new_size)
        else:
            sys.stderr.write('CAN\'T CONVERT IMAGE\n')
            return 0

    GetProc = dll.vlGetProc
    GetProc.argtypes = [VTFLibEnums.Proc]
    GetProc.restype = POINTER(c_int32)

    def get_proc(self, proc):
        try:
            return self.GetProc(proc).contents.value
        except:
            sys.stderr.write("ERROR IN GetProc\n")
            return -1

    SetProc = dll.vlSetProc
    SetProc.argtypes = [VTFLibEnums.Proc, POINTER(c_int32)]
    SetProc.restype = None

    def set_proc(self, proc, value):
        self.SetProc(proc, value)


if __name__ == '__main__':
    a = VTFLib()
    a.image_load(
        r"G:\SteamLibrary\SteamApps\common\SourceFilmmaker\game\usermod\materials\models\skuddbutt\mavis\body_clothed.vtf",
        False)
    print(a.image_format())
    print(ImageFlag(a.get_image_flags()).get_flag(ImageFlag.ImageFlagBorder))
    # a.image_save("G:\\SteamLibrary\\SteamApps\\common\\SourceFilmmaker\\game\\usermod\\materials\\models\\Red_eye\\Endless\\Feline\\Body2.vtf")
    print(a.get_last_error())
