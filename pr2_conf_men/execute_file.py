import os

from project.Get_options import Get_options

if __name__ == '__main__':
    with open("parameters.txt") as f:
        inp = f.read()
        exec = Get_options(inp)
        il = inp.split()
        d = exec.create_dict(il)
        exec.output(d)
