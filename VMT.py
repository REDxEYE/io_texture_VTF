import os
from pprint import pprint
try:
    from ValveFileSystem.path import Path
    from ValveFileSystem.valve import KeyValueFile,textureAsGameTexture
except:
    from .ValveFileSystem.valve import KeyValueFile,textureAsGameTexture
    from .ValveFileSystem.path import Path




class VMT:
    def __init__(self,filepath,game_dir = None):
        self.filepath = filepath.replace("/",'\\')
        if not game_dir:
            game_dir = str(self.filepath).replace(os.path.join(*Path(self.filepath).asContentModRelativePathFuzzy()),"")
        os.environ['VProject'] = str(game_dir)
        self.filepath = Path(self.filepath)
        self.textures = {}
        self.kv = KeyValueFile(filepath=filepath)
        self.shader = self.kv.getRootChunk().key
        self.material_data = self.kv.asDict()[self.shader]

    def parse(self):
        for key,value in self.material_data.items():
            if textureAsGameTexture(value):
                self.textures[key[1:].lower()] = textureAsGameTexture(value)

if __name__ == '__main__':
    # vmt = VMT(r'G:\SteamLibrary\SteamApps\common\SourceFilmmaker\game\usermod\materials\models\Red_eye\Endless\Qhala\normal body.vmt',r'G:\SteamLibrary\SteamApps\common\SourceFilmmaker\game\usermod')
    vmt = VMT(r'G:\SteamLibrary\SteamApps\common\SourceFilmmaker\game\usermod\materials\models\Red_eye\Xeno\Lewd_Xeno_male\Xenomorph_D.vmt')
    vmt.parse()
    pprint(vmt.textures)
