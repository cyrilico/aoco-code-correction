from .parameter import parameter

class array_parameter(parameter):
    """Array subroutine parameter"""

    def __init__(self, idx, element_type, is_output):
        super().__init__(idx)
        self.element_type = element_type
        if element_type =='char':
            self.printf_format = 'c' 
        elif element_type == 'int':
            self.printf_format = 'd'
        else:
            self.printf_format = 'f'
        self.is_output = is_output
    
    def get_prototype_representation(self):
        return '{}* arg{}'.format(self.element_type, self.idx)

    def get_test_declaration_representation(self):
        return '{} arg{}[] = {{{{ {{}} }}}};'.format(self.element_type, self.idx) if self.is_output else ''
    
    def get_test_call_representation(self):
        return 'arg{}'.format(self.idx) if self.is_output else '({}[]){{{{ {{}} }}}}'.format(self.element_type)
    
    def get_literal_representantion(self, value):
        return ','.join(map(str, value)) if self.printf_format != 'c' else ','.join(map(lambda x: "'{}'".format(x), value))

    def get_test_call_output_representation(self):
        var_name = 'arg{}'.format(self.idx)
        array_size = 'sizeof({})/sizeof({}[0])'.format(var_name, var_name)
        return '{}{}{}'.format(\
                    'printf("[");',
                    'for(int i = 0; i < {}; ++i) printf("%{}%s", {}[i], (i < {} - 1 ? "," : "\\0"));'.format(array_size, self.printf_format, var_name, array_size), \
                    'printf("]");')\
            if self.is_output else ''
