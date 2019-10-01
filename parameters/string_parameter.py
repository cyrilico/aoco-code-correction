from .parameter import parameter

class string_parameter(parameter):
    """String subroutine parameter"""

    def __init__(self, idx, is_output):
        super().__init__(idx)
        self.is_output = is_output
    
    def get_prototype_representation(self):
        return 'char* arg{}'.format(self.idx)

    def get_test_declaration_representation(self, value, test_idx):
        return 'char* test{}_arg{} = "{}";'.format(test_idx, self.idx, value) if self.is_output else ''