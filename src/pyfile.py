class Pyfile(object):

    def __init__(self, abs_path, root):
        self._absolute = abs_path
        self._root = root
        self._extract_module()

    def __repr__(self):
        return self._relative

    @property
    def relative(self):
        return self._relative

    @property
    def module(self):
        return self._module

    def lines(self):
        if hasattr(self, '_lines'):
            return self._lines
        with open(self._absolute, 'r') as f:
            self._lines = f.read().splitlines()
        return self._lines

    def _extract_module(self):
        if self._root.endswith('/'):
            self._root = self._root.rstrip('/')
        self._relative = self._absolute.replace(self._root + '/', '')
        self._module = self._relative[:-3].replace('/', '.')
