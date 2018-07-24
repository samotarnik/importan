import re


class Parser(object):

    COMMENT_LINE = re.compile('\s*#')

    def __init__(self, module, lines):
        self._module = module
        self._lines = lines

    def extract(self):
        if hasattr(self, '_imports'):
            return self._imports
        self._normalize_lines()
        self._parse()
        return self._imports

    def _normalize_lines(self):
        lines, stack = [], []
        for line in self._lines:
            if self._empty_or_comment(line):
                continue

            stack.append(line)
            if 'import ' in line and line.endswith('\\'):
                continue
            else:
                lines.append(self._handle_multiline(stack))
                stack = []
        self._lines = lines

    def _empty_or_comment(self, line):
        return not line or self.COMMENT_LINE.match(line)

    def _handle_multiline(self, lines):
        return ' '.join([l.rstrip('\\') for l in lines])

    def _parse(self):
        simp_imp = re.compile('import\s+([\w\.\,\s]+)')
        from_imp = re.compile('from\s+([\w\.]+)\s+import\s+([\w\.\,\s]+)')
        imports = set([])
        for line in self._lines:
            m = simp_imp.match(line)
            if m:
                raw = m.groups()[0].split(',')
                raw = [r.strip() for r in raw]
                imports.update(raw)
                continue
            m = from_imp.match(line)
            if m:
                base = m.groups()[0]
                tail = m.groups()[1].split(',')
                tail = [t.strip() for t in tail]
                tail = [t.split(' as ')[0] for t in tail]
                if base == '.':
                    base = self._module
                base = base + '.'
                for t in tail:
                    imports.add((base+t).split(' as ')[0])
        self._imports = imports
