from .subroutine import subroutine
from parameters.string_parameter import string_parameter as String
from parameters.numeric_parameter import numeric_parameter as Numeric
from parameters.array_parameter import array_parameter as Array

class numeric_subroutine(subroutine):
    """Subroutine that returns a single numeric value (e.g., int, float, double)"""

    def __init__(self, name, parameters, test_inputs, return_type):
        super().__init__(name, parameters, test_inputs)
        self.c_function_return = return_type
        self.printf_format = 'd' if return_type == 'int' else 'f'

    def build_test_calls(self):
       #for test_idx, test_input in enumerate(self.test_inputs):
       #    for test_value, parameter in zip(test_input, self.parameters):
       #        parameter.get_test_call_representation(test_value, test_idx)

        return ''.join(['printf("%{}\\n", {}({}));'.format(self.printf_format, self.name, \
                    ','.join([parameter.get_test_call_representation(test_value, test_idx) for test_value, parameter in zip(test_input, self.parameters)])) \
                for test_idx, test_input in enumerate(self.test_inputs)])
    
    def process_parameters(self, parameters):
        for idx, parameter in enumerate(parameters):
            if parameter == 'string':
                self.parameters.append(String(idx, False))
            elif parameter == 'array':
                self.parameters.append(Array(idx, parameter.replace('array','').strip(), False))
            else: #numeric
                self.parameters.append(Numeric(idx, parameter))