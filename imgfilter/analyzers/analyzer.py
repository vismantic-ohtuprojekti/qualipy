class Analyzer():
    def __init__(self):
        name = 'invalid'
        data = None
    
    def run(self, image_data):
        pass
    
    def get_copy(self):
        return np.copy(self.data)

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
            and self.name == other.name)

    def __ne__(self, other):
        return not self.__eq__(other)
