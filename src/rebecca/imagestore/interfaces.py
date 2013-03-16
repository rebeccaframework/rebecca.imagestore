from zope.interface import Interface


class IImageStore(Interface):
    def save(name, image):
        """ save image named ``name`` """


    def load(name):
        """ load image name ``name`` """

    def load_thumbnail(name):
        """ load image name ``name`` with thumbnailed size."""
