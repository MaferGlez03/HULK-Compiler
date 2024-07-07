import os
import sys
import dill


class PKL_Files:
    # use:
    # PKL_Files.save_object(lexer, "lexer")
    def save_object(object, object_name):
        sys.setrecursionlimit(10000)
        if not os.path.exists(object_name):
            os.makedirs(object_name)
        with open(f'.\\{object_name}.pkl', 'wb') as file_pkl:
            dill.dump(object, file_pkl)
    
    # use:
    # PKL_Files.load_object("lexer")
    def load_object(object_name):
        with open(f'{object_name}.pkl', 'rb') as file_pkl:
            return dill.load(file_pkl)
