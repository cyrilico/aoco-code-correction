from .subroutine import subroutine
from parameters.string_parameter import string_parameter as String
from parameters.numeric_parameter import numeric_parameter as Numeric
from parameters.array_parameter import array_parameter as Array

class mixed_subroutine(subroutine):
    """Subroutine that returns both a numeric value and one or more arrays"""

    def __init__(self, name, parameters, test_inputs, return_type):
        super().__init__(name, parameters, test_inputs)
        self.output = return_type

    def build_test_calls(self):
        """Method where subroutines implement the calls to test the input data and print out the calls' results"""
        #TODO: Structure should be: for all parameters do get_test_declaration_representation, then make the call. Incorporate printf accordingly
        pass
    
    def process_parameters(self, parameters):
        #TODO Update
        for idx, parameter in enumerate(parameters):
            if parameter == 'string':
                self.parameters.append(string_parameter(idx, False))
            elif parameter == 'array':
                self.parameters.append(array_parameter(idx, parameter.replace('array','').strip(), False))
            else: #numeric
                self.parameters.append(numeric_parameter(idx, parameter))