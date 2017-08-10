import importlib

try:
    import bpy
except Exception:
    bpy = None
import os, sys

import time
import os




def getpath() -> str:
    """

    Returns:
        str: path to current file
    """
    script_file = os.path.realpath(__file__)
    return os.path.dirname(script_file)


sys.path.append(getpath())
try:
    import progressBar
except:
    from . import progressBar
import io
import struct
import squish
import converter
import VTF_DATA

split = lambda A, n=3: [A[i:i + n] for i in range(0, len(A), n)]
def flip(data, x, y, chan):
    return [inner for outer in converter.split(list(data), (x * chan))[::-1] for inner in outer]
def convert_pixels(data):
    # return list(map(lambda a:a/256,data))
    return [a/256 for a in data]
class VTF:
    def readASCII(self, len_):
        return ''.join([self.readACSIIChar() for _ in range(len_)])

    def ReadByte(self):
        type_ = 'b'
        return struct.unpack(type_, self.data.read(struct.calcsize(type_)))[0]

    def readBytes(self, len_):
        type_ = 'b'
        return [struct.unpack(type_, self.data.read(struct.calcsize(type_)))[0] for _ in range(len_)]

    def readUByte(self):
        type_ = 'B'
        return struct.unpack(type_, self.data.read(struct.calcsize(type_)))[0]

    def ReadInt32(self):
        type_ = 'i'
        return struct.unpack(type_, self.data.read(struct.calcsize(type_)))[0]

    def readUInt32(self):
        type_ = 'I'
        return struct.unpack(type_, self.data.read(struct.calcsize(type_)))[0]

    def ReadShort(self):
        type_ = 'h'
        return struct.unpack(type_, self.data.read(struct.calcsize(type_)))[0]

    def readUInt16(self):
        type_ = 'H'
        return struct.unpack(type_, self.data.read(struct.calcsize(type_)))[0]

    def ReadFloat(self):
        type_ = 'f'
        return struct.unpack(type_, self.data.read(struct.calcsize(type_)))[0]

    def readACSIIChar(self):
        a = self.readUByte()
        return chr(a)

    def __init__(self, file: str):
        self.file_name = file.split(os.sep)[-1].split('.')[0]
        self.data = open(file, 'rb')
        self.data.seek(0, io.SEEK_END)
        self.filesize = self.data.tell()
        self.data.seek(0, io.SEEK_SET)
        self.vtf_header = self.readHeader()

        self.readFlags()
        self.readImage(self.vtf_header.mipmapCount)
        # self.import_texture()

    def readHeader(self):
        vtf_header = VTF_DATA.VTF_HEADER()
        vtf_header.signature = ''.join([chr(self.ReadByte()) for _ in range(4)])
        vtf_header.version = int(''.join(map(str,[self.ReadInt32() for _ in range(2)])))
        vtf_header.headerSize = self.ReadInt32()
        vtf_header.width = self.ReadShort()
        vtf_header.height = self.ReadShort()
        vtf_header.flags = self.ReadInt32()
        vtf_header.frames = self.ReadShort()
        vtf_header.firstFrame = self.ReadShort()
        vtf_header.padding0 = [self.ReadByte() for _ in range(4)]
        vtf_header.reflectivity = [self.ReadFloat() for _ in range(3)]
        vtf_header.padding1 = [self.ReadByte() for _ in range(4)]
        vtf_header.bumpmapScale = self.ReadFloat()
        vtf_header.highResImageFormat = self.ReadInt32()
        vtf_header.mipmapCount = self.ReadByte()
        vtf_header.lowResImageFormat = self.ReadInt32()
        vtf_header.lowResImageWidth = self.ReadByte()
        vtf_header.lowResImageHeight = self.ReadByte()
        if vtf_header.version >71:
            vtf_header.depth = self.ReadShort()
            vtf_header.padding2 = [self.ReadByte() for _ in range(3)]
            vtf_header.numResources = self.ReadInt32()
        print(vtf_header.__dict__)
        return vtf_header

    def readFlags(self):
        self.flags = VTF_DATA.VTF_FLAGS.getFlags(self.vtf_header.flags)

    @staticmethod
    def calcImageSize(width, height, depth, format):
        if format == 'DXT5':
            return int((width / 4) * (height / 4) * 16 * depth)
        if format == 'DXT1':
            return int((width / 4) * (height / 4) * 8 * depth)

    def readImage(self,mipmapCount):
        self.data.seek(self.vtf_header.headerSize)
        print(VTF_DATA.VTF_FORMATS(self.vtf_header.highResImageFormat).name)
        print(self.flags)
        # if 'NOMIP' in self.flags:
        if self.vtf_header.mipmapCount <= 1:
            data = self.data.read()
        else:

            if VTF_DATA.VTF_FORMATS(self.vtf_header.highResImageFormat).name == 'DXT5':
                off = self.calcImageSize(self.vtf_header.width, self.vtf_header.height, self.vtf_header.depth, 'DXT5')
                print(off)
                self.data.seek(-off, io.SEEK_END)
                data = self.data.read()

            elif VTF_DATA.VTF_FORMATS(self.vtf_header.highResImageFormat).name == 'DXT1':
                off = self.calcImageSize(self.vtf_header.width, self.vtf_header.height, self.vtf_header.depth, 'DXT1')
                print(off)
                self.data.seek(-off, io.SEEK_END)
                data = self.data.read()
            else:
                print('kek')
                data = self.data.read()
                # print(data[:250])
        if VTF_DATA.VTF_FORMATS(self.vtf_header.highResImageFormat).name == 'DXT5':
            print('DECOMPRES DXT5')
            data = squish.decompressImage(data, self.vtf_header.width, self.vtf_header.height, squish.DXT5)
            mode = 'RGBA'
        elif VTF_DATA.VTF_FORMATS(self.vtf_header.highResImageFormat).name == 'DXT3':
            print('DECOMPRES DXT3')
            data = squish.decompressImage(data, self.vtf_header.width, self.vtf_header.height, squish.DXT3)
            mode = 'RGBA'
        elif VTF_DATA.VTF_FORMATS(self.vtf_header.highResImageFormat).name == 'DXT1':
            print('DECOMPRES DXT1')
            print(len(data))
            data = squish.decompressImage(data, self.vtf_header.width, self.vtf_header.height, squish.DXT1)
            mode = 'RGBA'
        elif VTF_DATA.VTF_FORMATS(self.vtf_header.highResImageFormat).name == 'RGBA8888':
            print('Reading RGBA8888')
            mode = 'RGBA'
            data = data
        # elif VTF_DATA.VTF_FORMATS(self.vtf_header.highResImageFormat).name == 'RGB888':
        #     print('Reading RGB888')
        #     mode = 'RGBA'
        #     print(len(data))
        #     a = time.time()
        #     data = converter.rgb2rgba(data)
        #     print((time.time()-a)*1000,'ms')
        #     data = data
        else:
            raise NotImplementedError('Format {} currently is not supported'.format(
                VTF_DATA.VTF_FORMATS(self.vtf_header.highResImageFormat).name))
        # print('DONE DECOMPRESSING')
        self.IMAGE = data
        self.MODE = mode
        # print(len(data))


    def import_texture(self):
        # from PIL import Image
        a = time.time()
        acc = []
        rows = converter.split(self.IMAGE,self.vtf_header.width*len(self.MODE))[::-1]
        for row in rows:
            acc.extend(row)
        print('Dims',self.vtf_header.width,'x',self.vtf_header.height)
        print((time.time()-a)*1000,'ms')
        # IMAGE = Image.frombytes(self.MODE, (self.vtf_header.width, self.vtf_header.height), bytes(self.IMAGE))
        # IMAGE.save(
        #     '{}_{}.png'.format(self.file_name, VTF_DATA.VTF_FORMATS(self.vtf_header.highResImageFormat).name))
        image = bpy.data.images.new(self.file_name, width=self.vtf_header.width, height=self.vtf_header.height)
        size = len(image.pixels)//8
        field = progressBar.Progress_bar('Importing {} texture'.format(self.file_name),8,20)
        for n in range(0,len(image.pixels),size):
            image.pixels[n:n+size] = converter.convert_pixels(acc[n:n+size])
            field.increment(1)
            field.draw()
        image.pack(as_png = True)
        return image
        # image.filepath = "//{}_{}.png".format(self.file_name, VTF_DATA.VTF_FORMATS(self.vtf_header.highResImageFormat).name)
        # image.file_format = 'PNG'
        # image.save()

if __name__ == '__main__':
    a = VTF(r"E:\PYTHON\VTF_reader\test_data\xenosoldier_armor_a_n.vtf")
    print(a.vtf_header.__dict__)
    print(a.flags)
    print('SUCCESS')
