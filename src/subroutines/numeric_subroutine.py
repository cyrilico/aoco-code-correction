from .subroutine import subroutine
from parameters.string_parameter import string_parameter as String
from parameters.numeric_parameter import numeric_parameter as Numeric
from parameters.array_parameter import array_parameter as Array

class numeric_subroutine(subroutine):
    """Subroutine that returns a single numeric value (e.g., int, float, double)"""

    def __init__(self, name, parameters, return_type):
        super().__init__(name, parameters)
        self.c_function_return = return_type
        self.printf_format = 'd' if return_type == 'int' else 'f'

    def get_nr_outputs(self):
        return 0

    def build_test_call(self):
        return 'printf("%{}\\n", {}({}));'.format(self.printf_format, self.name, \
                    ','.join([parameter.get_test_call_representation() for parameter in self.parameters]))
    
    def process_parameters(self, parameters):
        for idx, parameter in enumerate(parameters):
            if parameter == 'string':
                self.parameters.append(String(idx, False))
            elif 'array' in parameter:
                self.parameters.append(Array(idx, parameter.replace('array','').strip(), False))
            else: #numeric
                self.parameters.append(Numeric(idx, parameter))
    
    def compare_outputs(self, expected, real, precision):
        if(len(real) != len(expected)):
            return False
        if self.c_function_return == 'int':
            return expected[0] == int(real[0])
        else:
            return abs(expected[0] - float(real[0])) <= precision
