from .parameter import parameter

class string_parameter(parameter):
    """String subroutine parameter"""

    def __init__(self, idx, is_output):
        super().__init__(idx)
        self.is_output = is_output
    
    def get_prototype_representation(self):
        return 'char* arg{}'.format(self.idx)

    def get_test_declaration_representation(self):
        return 'char arg{}[] = "{{}}";'.format(self.idx) if self.is_output else ''
    
    def get_test_call_representation(self):
        return 'arg{}'.format(self.idx) if self.is_output else '"{}"'
    
    def get_literal_representantion(self, value):
        return value

    def get_test_call_output_representation(self):
        return 'printf("%s", arg{});'.format(self.idx) if self.is_output else ''
