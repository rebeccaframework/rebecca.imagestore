import os
from PIL import Image
from zope.interface import implementer
from repoze.filesafe import create_file, open_file
from .interfaces import IImageStore


@implementer(IImageStore)
class DirectoryImageStore(object):
    def __init__(self, basedir, thumbnail_size=(128, 128)):
        self.basedir = basedir
        self.thumbnail_size = thumbnail_size

    def _filepath(self, name):
        return os.path.abspath(os.path.join(self.basedir, name))

    def save(self, name, image):
        with create_file(self._filepath(name)) as f:
            f.write(image.tostring())

    def load(self, name):
        with open_file(self._filepath(name)) as f:
            return Image.open(f)
