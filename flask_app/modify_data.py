import numpy as np
import pandas as pd


def modify_result(result, keys, values):
    dictionary = dict(zip(keys, values))
    dictionary.update({'result':result[0]})
    dictionary.update({'Spruce/Fir':dictionary[0.0], 'Lodgepole Pine':dictionary[1.0],'Ponderosa Pine':dictionary[2.0], 'Cottonwood/Willow':dictionary[3.0],  'Aspen':dictionary[4.0],'Douglas-fir':dictionary[5.0], 'Krummholz':dictionary[6.0], })
    dictionary.pop(0.0,None)
    dictionary.pop(1.0,None)
    dictionary.pop(2.0,None)
    dictionary.pop(3.0,None)
    dictionary.pop(4.0,None)
    dictionary.pop(5.0,None)
    dictionary.pop(6.0,None)
    return dictionary

if __name__ == '__main__':
    print('Please do not call me directly')
