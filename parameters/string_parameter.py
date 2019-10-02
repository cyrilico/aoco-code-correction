from .parameter import parameter

class string_parameter(parameter):
    """String subroutine parameter"""

    def __init__(self, idx, is_output):
        super().__init__(idx)
        self.is_output = is_output
    
    def get_prototype_representation(self):
        return 'char* arg{}'.format(self.idx)

    def get_test_declaration_representation(self, value, test_idx):
        return 'char test{}_arg{}[] = "{}";'.format(test_idx, self.idx, value) if self.is_output else ''
    
    def get_test_call_representation(self, value, test_idx):
        return 'test{}_arg{}'.format(test_idx, self.idx) if self.is_output else value
    
    def get_test_call_output_representation(self, test_idx):
        return 'printf("%s", test{}_arg{});'.format(test_idx, self.idx) if self.is_output else ''