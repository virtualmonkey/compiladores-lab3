class Class:
    def __init__(
        self,
        name,
        inheritsFrom = 'IO',
        size = 0
    ):
        self.name = name
        self.inheritsFrom = inheritsFrom
        self.size = size

    def __str__(self):
        return '[CLASS] -> Identifier: %s, inheritsFrom: %s, size: %s' % (self.name, self.inheritsFrom, self.size)