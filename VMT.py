import os
from pprint import pprint

try:
    from ValveUtils import KeyValueFile, GameInfoFile
except:
    from .ValveUtils import KeyValueFile, GameInfoFile
from pathlib import Path

del os.environ['VProject']


class VMT:

    def _get_proj_root(self, path: Path):
        if path.parts[-1] == 'materials':
            return path.parent
        else:
            return self._get_proj_root(path.parent)

    def __init__(self, filepath, game_dir=None):
        self.filepath = Path(filepath)
        if not game_dir:
            game_dir = self._get_proj_root(self.filepath)
        os.environ['VProject'] = str(game_dir)
        self.textures = {}
        self.kv = KeyValueFile(filepath=filepath)
        self.shader = self.kv.root_chunk.key
        self.material_data = self.kv.as_dict[self.shader]
        self.gameinfo = GameInfoFile(game_dir / 'gameinfo.txt')

    def parse(self):
        print(self.shader)
        for key, value in self.material_data.items():
            if type(value) is str:
                texture = self.gameinfo.find_texture(value)
                if texture:
                    self.textures[key] = texture
                    # print(texture)
            # if textureAsGameTexture(value):
            #     self.textures[key[1:].lower()] = textureAsGameTexture(value)


if __name__ == '__main__':
    # vmt = VMT(r'G:\SteamLibrary\SteamApps\common\SourceFilmmaker\game\usermod\materials\models\Red_eye\Endless\Qhala\normal body.vmt',r'G:\SteamLibrary\SteamApps\common\SourceFilmmaker\game\usermod')
    vmt = VMT(
        r'G:\SteamLibrary\SteamApps\common\SourceFilmmaker\game\usermod\materials\models\Red_eye\Xeno\Lewd_Xeno_male\Xenomorph_D.vmt')
    vmt.parse()
    pprint(vmt.textures)
