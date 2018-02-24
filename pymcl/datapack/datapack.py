import os
import shutil
import zipfile

from pymcl.datapack.packfile import IndexFile
from . import packfile


class Datapack:
    def __init__(self):
        self.files = []
        self.add_file(IndexFile())

    def add_file(self, pack):
        if isinstance(pack, packfile.PackFile):
            self.files.append(pack)
        elif hasattr(pack, "to_packfile"):
            self.files.append(pack.to_packfile())
        else:
            raise ValueError(f'''can't add type {pack.__class__} to datapack''')

    def create_output_files(self):
        if not os.path.exists("output"):
            os.mkdir("output")
        else:
            shutil.rmtree("output")
            os.mkdir("output")
        for f in self.files:
            f: packfile.PackFile
            f.save_to_outfolder("output")

    def generate_datapack(self):
        with zipfile.ZipFile("output.zip", 'w') as z:
            for i in self.files:
                i: packfile.PackFile
                z.writestr(i.real_path(), i.get_content())
