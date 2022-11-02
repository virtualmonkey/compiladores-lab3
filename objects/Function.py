class Function:
    def __init__(
        self,
        id,
        name,
        type,
        scope = None,
        isFrom = None
    ):
        self.id = id
        self.name = name
        self.type = type
        self.scope = scope
        self.isFrom = isFrom
    def __str__(self):
        return '[FUNCTION] -> identifier: %s, type: %s, scope: %s, isFrom: %s' % (self.name, self.type, self.scope, self.isFrom)