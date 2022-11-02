class Error:
    def __init__(self, type, line, message):
        self.type = type
        self.line = line
        self.message = message
    
    def __str__(self):
        return '%s error found in line %s: %s' % (self.type, self.line, self.message)