def array_transladada(array:list):

    array_transladada = array.copy()

    i = 0
    while i < len(array) + 1:

        array_transladada = [array_transladada[-1]] + array_transladada[:-1]
        print(array_transladada)

        if array_transladada == array:
            break
        
    
numeros = [1,2,3,4,5,6,7,8,9,10] 
array_transladada(numeros)


import numpy as np


for i in range(len(numeros) + 1):
    
    a = np.roll(numeros,i)
    print(a)



