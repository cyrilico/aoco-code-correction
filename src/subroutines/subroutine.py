class subroutine:
    """Abstract parent class that defines a generic subroutine and all the methods it should implement"""

    def __init__(self, name, parameters):
        self.name = name
        self.parameters_raw = parameters
        self.c_function_return = "void" #By default, no return value in C function. To be overriden by subclasses when necessary
        self.parameters = []
    
    def get_nr_outputs(self):
        """Method that returns number of non int outputs"""
        pass
    
    def build_c_file(self):
        self.process_parameters(self.parameters_raw)
        return '{} {} {}'.format(\
                self.build_headers(),\
                self.build_prototype(),\
                'int main() {{{{ {} return 0;}}}}'.format(self.build_test_call()))
    
    def build_headers(self):
        return '#include <stdio.h>\n'

    def build_prototype(self):
        return 'extern {} {}({});\n'.format(self.c_function_return, self.name, ','.join(map(lambda p: p.get_prototype_representation(), self.parameters)))
    
    def build_test_call(self):
        """Method where subroutines implement the calls to test the input data and print out the calls' results"""
        pass

    def process_parameters(self, parameters):
        """Method where subroutines create argument objects for each type. Depending on subroutine type might be an output too."""
        pass

    def compare_outputs(self, expected, real, precision):
        """Method that, given an instance of test outputs, compares to see if the real results match the expected ones"""
        pass