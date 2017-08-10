# char    signature[4]
# unsigned int    version[2]
# unsigned int    headerSize
# unsigned short    width
# unsigned short    height
# unsigned int    flags
# unsigned short    frames
# unsigned short    firstFrame
# unsigned char    padding0[4]
# float    reflectivity[3]
# unsigned char    padding1[4]
# float    bumpmapScale
# unsigned int    highResImageFormat
# unsigned char    mipmapCount
# unsigned int    lowResImageFormat
# unsigned char    lowResImageWidth
# unsigned char    lowResImageHeight
# unsigned short    depth
# unsigned char    padding2[3]
# unsigned int    numResources
#   IMAGE_FORMAT_RGBA8888 = 0,				//!<  = Red, Green, Blue, Alpha - 32 bpp
# 	IMAGE_FORMAT_ABGR8888,					//!<  = Alpha, Blue, Green, Red - 32 bpp
# 	IMAGE_FORMAT_RGB888,					//!<  = Red, Green, Blue - 24 bpp
# 	IMAGE_FORMAT_BGR888,					//!<  = Blue, Green, Red - 24 bpp
# 	IMAGE_FORMAT_RGB565,					//!<  = Red, Green, Blue - 16 bpp
# 	IMAGE_FORMAT_I8,						//!<  = Luminance - 8 bpp
# 	IMAGE_FORMAT_IA88,						//!<  = Luminance, Alpha - 16 bpp
# 	IMAGE_FORMAT_P8,						//!<  = Paletted - 8 bpp
# 	IMAGE_FORMAT_A8,						//!<  = Alpha- 8 bpp
# 	IMAGE_FORMAT_RGB888_BLUESCREEN,			//!<  = Red, Green, Blue, "BlueScreen" Alpha - 24 bpp
# 	IMAGE_FORMAT_BGR888_BLUESCREEN,			//!<  = Red, Green, Blue, "BlueScreen" Alpha - 24 bpp
# 	IMAGE_FORMAT_ARGB8888,					//!<  = Alpha, Red, Green, Blue - 32 bpp
# 	IMAGE_FORMAT_BGRA8888,					//!<  = Blue, Green, Red, Alpha - 32 bpp
# 	IMAGE_FORMAT_DXT1,						//!<  = DXT1 compressed format - 4 bpp
# 	IMAGE_FORMAT_DXT3,						//!<  = DXT3 compressed format - 8 bpp
# 	IMAGE_FORMAT_DXT5,						//!<  = DXT5 compressed format - 8 bpp
# 	IMAGE_FORMAT_BGRX8888,					//!<  = Blue, Green, Red, Unused - 32 bpp
# 	IMAGE_FORMAT_BGR565,					//!<  = Blue, Green, Red - 16 bpp
# 	IMAGE_FORMAT_BGRX5551,					//!<  = Blue, Green, Red, Unused - 16 bpp
# 	IMAGE_FORMAT_BGRA4444,					//!<  = Red, Green, Blue, Alpha - 16 bpp
# 	IMAGE_FORMAT_DXT1_ONEBITALPHA,			//!<  = DXT1 compressed format with 1-bit alpha - 4 bpp
# 	IMAGE_FORMAT_BGRA5551,					//!<  = Blue, Green, Red, Alpha - 16 bpp
# 	IMAGE_FORMAT_UV88,						//!<  = 2 channel format for DuDv/Normal maps - 16 bpp
# 	IMAGE_FORMAT_UVWQ8888,					//!<  = 4 channel format for DuDv/Normal maps - 32 bpp
# 	IMAGE_FORMAT_RGBA16161616F,				//!<  = Red, Green, Blue, Alpha - 64 bpp
# 	IMAGE_FORMAT_RGBA16161616,				//!<  = Red, Green, Blue, Alpha signed with mantissa - 64 bpp
# 	IMAGE_FORMAT_UVLX8888,					//!<  = 4 channel format for DuDv/Normal maps - 32 bpp
# 	IMAGE_FORMAT_R32F,						//!<  = Luminance - 32 bpp
# 	IMAGE_FORMAT_RGB323232F,				//!<  = Red, Green, Blue - 96 bpp
# 	IMAGE_FORMAT_RGBA32323232F,				//!<  = Red, Green, Blue, Alpha - 128 bpp
# 	IMAGE_FORMAT_NV_DST16,
# 	IMAGE_FORMAT_NV_DST24,
# 	IMAGE_FORMAT_NV_INTZ,
# 	IMAGE_FORMAT_NV_RAWZ,
# 	IMAGE_FORMAT_ATI_DST16,
# 	IMAGE_FORMAT_ATI_DST24,
# 	IMAGE_FORMAT_NV_NULL,
# 	IMAGE_FORMAT_ATI2N,
# 	IMAGE_FORMAT_ATI1N,
from enum import Enum, IntEnum
from typing import List
class VTF_FLAGS:
    POINTSAMPLE = 0x00000001,
    TRILINEAR = 0x00000002,
    CLAMPS = 0x00000004,
    CLAMPT = 0x00000008,
    ANISOTROPIC = 0x00000010,
    HINT_DXT5 = 0x00000020,
    SRGB = 0x00000040,
    DEPRECATED_NOCOMPRESS = 0x00000040,
    NORMAL = 0x00000080,
    NOMIP = 0x00000100,
    NOLOD = 0x00000200,
    MINMIP = 0x00000400,
    PROCEDURAL = 0x00000800,
    ONEBITALPHA = 0x00001000,
    EIGHTBITALPHA = 0x00002000,
    ENVMAP = 0x00004000,
    RENDERTARGET = 0x00008000,
    DEPTHRENDERTARGET = 0x00010000,
    NODEBUGOVERRIDE = 0x00020000,
    SINGLECOPY = 0x00040000,
    UNUSED0 = 0x00080000,
    DEPRECATED_ONEOVERMIPLEVELINALPHA = 0x00080000,
    UNUSED1 = 0x00100000,
    DEPRECATED_PREMULTCOLORBYONEOVERMIPLEVEL = 0x00100000,
    UNUSED2 = 0x00200000,
    DEPRECATED_NORMALTODUDV = 0x00200000,
    UNUSED3 = 0x00400000,
    DEPRECATED_ALPHATESTMIPGENERATION = 0x00400000,
    NODEPTHBUFFER = 0x00800000,
    UNUSED4 = 0x01000000,
    DEPRECATED_NICEFILTERED = 0x01000000,
    CLAMPU = 0x02000000,
    VERTEXTEXTURE = 0x04000000,
    SSBUMP = 0x08000000,
    UNUSED5 = 0x10000000,
    DEPRECATED_UNFILTERABLE_OK = 0x10000000,
    BORDER = 0x20000000,
    DEPRECATED_SPECVAR_RED = 0x40000000,
    DEPRECATED_SPECVAR_ALPHA = 0x80000000,
    LAST = 0x20000000,
    @staticmethod
    def getFlags(flags):
        DFlags = []

        vars_ = {var:VTF_FLAGS.__dict__[var] for var in vars(VTF_FLAGS) if not var.startswith('_') and var.isupper()}
        for var,int_ in vars_.items():
            if (flags & int_[0])>0:
                DFlags.append(var)
        return DFlags


class VTF_FORMATS(IntEnum):
    RGBA8888 = 0
    ABGR8888 = 1
    RGB888 = 2
    BGR888 = 3
    RGB565 = 4
    I8 = 5
    IA88 = 6
    P8 = 7
    A8 = 8
    RGB888_BLUESCREEN = 9
    BGR888_BLUESCREEN = 10
    ARGB8888 = 11
    BGRA8888 = 12
    DXT1 = 13
    DXT3 = 14
    DXT5 = 15
    BGRX8888 = 16
    BGR565 = 17
    BGRX5551 = 18
    BGRA4444 = 19
    DXT1_ONEBITALPHA = 20
    BGRA5551 = 21
    UV88 = 22
    UVWQ8888 = 23
    RGBA16161616F = 24
    RGBA16161616 = 25
    UVLX8888 = 26
    R32F = 27
    RGB323232F = 28
    RGBA32323232F = 29
    NV_DST16 = 30
    NV_DST24 = 31
    NV_INTZ = 32
    NV_RAWZ = 33
    ATI_DST16 = 34
    ATI_DST24 = 35
    NV_NULL = 36
    ATI2N = 37
class VTF_HEADER:
    def __init__(self):
        self.signature = []  # type: List[str]*4
        self.version = []  # type: List[int]*2
        self.headerSize = 0
        self.width = 0
        self.height = 0
        self.flags = 0
        self.frames = 0
        self.firstFrame = 0
        self.padding0 = []  # type: List[int]*4
        self.reflectivity = []  # type: List[int]*3
        self.padding1 = []  # type: List[int]*4
        self.bumpmapScale = 0.0
        self.mipmapCount = 0
        self.highResImageFormat = 0
        self.lowResImageFormat = 0
        self.lowResImageWidth = 0
        self.lowResImageHeight = 0
        self.depth = 1
        self.padding2 = [] # type: List[int]*3
        self.numResources = 0