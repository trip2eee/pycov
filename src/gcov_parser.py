from lib2to3.pgen2 import token


class GCOVParser:
    """GCC/G++ GCOV file parser.
    """
    def __init__(self, file_path):
        self.file_path = file_path
        
        self.num_lines = 0              # the number of lines
        self.num_lines_exec = 0         # the number of executed lines.

        self.num_branches = 0           # the number of branches
        self.num_branches_exec = 0      # the number of branches taken

        self.num_functions = 0          # the number of functions
        self.num_functions_exec = 0     # the number of functions called.

        self.src = ''

        self.parse(file_path)
        self.compute_metrics()

    def parse(self, file_path):

        with open(file_path, 'r') as f:
            line = f.readline()

            while line != '':
                tokens = line.split()

                if tokens[0] == 'function':
                    self.num_functions += 1
                    if tokens[3] != '0':
                        self.num_functions_exec += 1

                elif tokens[0] == 'branch':
                    self.num_branches += 1
                    if tokens[2] == 'taken' and tokens[3] != '0':
                        self.num_branches_exec += 1

                elif tokens[0] == 'call':
                    pass

                else:
                    if len(tokens) >= 2 and tokens[1][0] != '0':
                        idx_sep = line.find(':', 0)
                        idx_sep = line.find(':', idx_sep+1)
                        self.src += line[idx_sep+1:]

                        if tokens[0] != '-:':
                            self.num_lines += 1

                            if tokens[0] != '#####:':
                                self.num_lines_exec += 1

                
                line = f.readline()

    def compute_metrics(self):
        self.line_coverage = self.num_lines_exec / max(1, self.num_lines)
        self.function_coverage = self.num_functions_exec / max(1, self.num_functions)
        self.branch_coverage = self.num_branches_exec / max(1, self.num_branches)
