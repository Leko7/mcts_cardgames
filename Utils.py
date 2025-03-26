# Utils.py
import numpy as np

def one_hot(input_list, length):
    x = np.zeros((length),dtype=np.int64)
    for i in input_list:
        x[i] = 1
    return x

def hash(state):
    s = state.copy()
    s = s.tolist()
    return sum(bit * (2 ** (len(s) - 1 - i)) for i, bit in enumerate(s))