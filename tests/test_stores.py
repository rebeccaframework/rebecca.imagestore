import pytest
import mock
from testfixtures import TempDirectory, Replacer

class DummyImage(object):
    def __init__(self, data):
        self.data = data

    @classmethod
    def open(cls, s):
        return cls(s.read())

class TestDirectoryImageStore(object):
    @pytest.fixture
    def target(self):
        from rebecca.imagestore.stores import DirectoryImageStore
        return DirectoryImageStore

    @pytest.fixture
    def datamanager(self, request):
        from repoze.filesafe.testing import setupDummyDataManager, cleanupDummyDataManager
        def fin():
            cleanupDummyDataManager()
        request.addfinalizer(fin)
        return setupDummyDataManager()

    def test_it(self, target):
        store = target('/testing/path')
        assert store.basedir == '/testing/path'

    def test_filepath(self, target):
        with TempDirectory() as d:
            store = target(d.path)
            result = store._filepath('testing')
            assert result.startswith(d.path)
        
    def test_save(self, target):
        from repoze.filesafe import _get_manager
        import os
        datamanager = _get_manager()
        mock_image = mock.Mock()
        mock_image.tostring.return_value = b"this-is-test-data"
        with TempDirectory() as d:
            store = target(d.path)
            store.save('testing', mock_image)
            mock_image.tostring.assert_called_with()

            assert os.path.join(d.path, 'testing') in datamanager.vault


    def test_load(self, target):
        from repoze.filesafe import _get_manager
        import os
        datamanager = _get_manager()
        with Replacer() as r, TempDirectory() as d:
            with datamanager.createFile(os.path.join(d.path, 'testing'), "w") as f:
                f.write(b'test-data')

            r.replace('rebecca.imagestore.stores.Image', DummyImage)

            store = target(d.path)
            result = store.load('testing')
            assert result.data == b'test-data'
