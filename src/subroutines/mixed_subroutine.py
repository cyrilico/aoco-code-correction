from .subroutine import subroutine
from parameters.string_parameter import string_parameter as String
from parameters.numeric_parameter import numeric_parameter as Numeric
from parameters.array_parameter import array_parameter as Array

from ast import literal_eval

class mixed_subroutine(subroutine):
    """Subroutine that returns both a number and one or more arrays"""

    def __init__(self, name, parameters, number_return_type, array_outputs):
        super().__init__(name, parameters)
        self.c_function_return = number_return_type
        if number_return_type == 'int':
            self.printf_format = 'd'
        elif number_return_type == 'float' or number_return_type == 'double':
            self.printf_format = 'f'
        elif number_return_type == 'char':
            self.printf_format = 'c'
        self.array_outputs = array_outputs

    def get_nr_outputs(self):
        return len(self.array_outputs)

    def build_test_call(self):
        return '{} {} {} printf("\\n");'.format(\
                    #Declare output variables beforehand, so we have access to them after subroutine call
                    ''.join([parameter.get_test_declaration_representation() for parameter in self.parameters]),\
                    #Actually make subroutine call
                    'printf("%{}\\n",{}({}));'.format(self.printf_format, self.name, ','.join([parameter.get_test_call_representation() for parameter in self.parameters])),\
                    #Access previously declared variables to print their final values
                    'printf("\\n");'.join(filter(lambda x: x != '', [parameter.get_test_call_output_representation() for parameter in self.parameters])))
    
    def process_parameters(self, parameters):
        for idx, parameter in enumerate(parameters):
            if parameter == 'string':
                self.parameters.append(String(idx, True if idx >= (len(parameters) - len(self.array_outputs)) else False))
            elif 'array' in parameter:
                self.parameters.append(Array(idx, parameter.replace('array','').strip(), True if idx >= (len(parameters) - len(self.array_outputs)) else False))
            else: #numeric
                self.parameters.append(Numeric(idx, parameter))

    def compare_outputs(self, expected, real, precision):
        if(len(expected) != len(real)):
            return False
        if self.printf_format == 'd' and expected[0] != int(real[0]):
            return False
        elif self.printf_format == 'c':
            if expected[0] is None and real[0].rstrip('\x00') != "" and real[0] != '0':
                return False
            elif expected[0] is not None and expected[0] != real[0]:
                return False
        elif self.printf_format == 'f' and abs(expected[0]-float(real[0])) > precision:
            return False

        for out_type, exp, re in zip(self.array_outputs, expected[1:], real[1:]):
            if out_type == 'string': 
                if exp != re:
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

