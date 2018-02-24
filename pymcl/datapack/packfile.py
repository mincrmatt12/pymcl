import os


class PackFile:
    def real_path(self):
        return ""

    def get_content(self):
        return ""

    def save_to_outfolder(self, root):
        folder, name = os.path.split(self.real_path())
        if not os.path.exists(os.path.join(root, folder)):
            os.makedirs(os.path.join(root, folder))
        with open(os.path.join(root, folder, name), "w") as f:
            f.write(self.get_content())


class SimplePackFile(PackFile):
    def __init__(self, path, content):
        self.path = path
        self.content = content

    def get_content(self):
        return self.content

    def real_path(self):
        ns, path = self.path.split(":")
        return os.path.join("data", ns, path)


class IndexFile(PackFile):
    def __init__(self):
        pass

    def get_content(self):
        return """{
    "pack": {
        "pack_format": 1,
        "description": "MCL output pack"
    }
}"""

    def real_path(self):
        return "pack.mcmeta"
