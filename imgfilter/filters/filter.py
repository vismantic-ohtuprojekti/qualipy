class Filter(object):

    def __init__(self):
        parameters = {}

    def set_optional_parameters(self, optional_parameters):
        for key, value in optional_parameters.iteritems():
            if key not in parameters:
                raise ValueError("invalid parameter")
            parameters[key] = value
    
    def run(self):
        pass




