class subroutine:
    """Abstract parent class that defines a generic subroutine and all the methods it should implement"""

    c_function_return = "void" #By default, no return value in C function. To be overriden by subclasses when necessary
    parameters = []

    def __init__(self, name, parameters, test_inputs):
        self.name = name
        self.test_inputs = test_inputs
        self.file = open('{}.c'.format(self.name), 'w')
        self.parameters_raw = parameters
        self.parameters = []
    
    def build_c_file(self):
        self.process_parameters(self.parameters_raw)
        self.file.write('#include <stdio.h>\n')
        self.file.write(self.build_prototype())
        self.file.write('int main() {{ {} return 0;}}'.format(self.build_test_calls()))
        self.file.close()

    def build_prototype(self):
        return 'extern {} {}({});\n'.format(self.c_function_return, self.name, ','.join(map(lambda p: p.get_prototype_representation(), self.parameters)))
    
    def build_test_calls(self):
        """Method where subroutines implement the calls to test the input data and print out the calls' results"""
        #TODO: Structure should be: for all parameters do get_test_declaration_representation, then make the call. Incorporate printf accordingly
        pass

    def process_parameters(self, parameters):
        """Method where subroutines create argument objects for each type. Depending on subroutine type might be an output too."""
        pass