from .subroutine import subroutine
from parameters.string_parameter import string_parameter as String
from parameters.numeric_parameter import numeric_parameter as Numeric
from parameters.array_parameter import array_parameter as Array

from ast import literal_eval

class array_subroutine(subroutine):
    """Subroutine that returns one or more arrays"""

    def __init__(self, name, parameters, outputs):
        super().__init__(name, parameters)
        self.outputs = outputs

    def get_nr_outputs(self):
        return len(self.outputs)

    def build_test_call(self):
        return '{} {} {} printf("\\n");'.format(\
                    #Declare output variables beforehand, so we have access to them after subroutine call
                    ''.join([parameter.get_test_declaration_representation() for parameter in self.parameters]),\
                    #Actually make subroutine call
                    '{}({});'.format(self.name, ','.join([parameter.get_test_call_representation() for parameter in self.parameters])),\
                    #Access previously declared variables to print their final values
                    'printf("\\n");'.join(filter(lambda x: x != '', [parameter.get_test_call_output_representation() for parameter in self.parameters])))
    
    def process_parameters(self, parameters):
        for idx, parameter in enumerate(parameters):
            if parameter == 'string':
                self.parameters.append(String(idx, True if idx >= (len(parameters) - len(self.outputs)) else False))
            elif 'array' in parameter:
                self.parameters.append(Array(idx, parameter.replace('array','').strip(), True if idx >= (len(parameters) - len(self.outputs)) else False))
            else: #numeric
                self.parameters.append(Numeric(idx, parameter))

    def compare_outputs(self, expected, real, precision):
        if(len(expected) != len(real)):
            return False
        for out_type, exp, re in zip(self.outputs, expected, real):
            if out_type == 'string' and exp != real:
                return False
            else: #Array
                arr_type = out_type.replace('array','').strip()
                re_arr = literal_eval(re)
                if(len(exp) != len(re_arr)):
                    return False
                for exp_el, re_el in zip(exp, re_arr):
                    if arr_type == 'int' and exp_el != re_el:
                        return False
                    elif abs(exp_el-re_el) > precision:
                        return False
        
        return True
