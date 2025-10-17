import string
import math
import time
import codecs
from decimal import Decimal
from fractions import Fraction

def arr_namer(arr, names=list(string.ascii_lowercase)): # Parametro: Frecuencias.
    index, n, r = 0, 0, ''
    named_arr = list()
    #print("\nFrecuencias iniciales:\n")
    if names == list(string.ascii_lowercase):
        for element in arr:
            if index == 26:
                index = 0
                n += 1
                r = '{}'.format(n)
            #print('[{}] - {}'.format(names[index]+'{}'.format(r),element))
            yield [element,names[index]+'{}'.format(r)]
            index += 1
    else:
        for element, name in zip(arr, names):
            #print('[{}] - {}'.format(name,element))
            yield [element,name]

def best_pair(arr): # Arguments: frequencies with names.
    if len(arr) == 2:
        return [tuple(arr[0]),tuple(arr[1])]
    if len(arr) < 2:
        return arr
    current = 1
    for i, x in enumerate(arr):
        if i == 0 or i == len(arr)-1:
            pass
        else:
            left = 0
            for n in arr[:i]:
                left += n[0]
            right = 0
            for n in arr[i:]:
                right += n[0]
            if abs(left-right) < current:
                best = [tuple(arr[:i]), tuple(arr[i:])]
                current = abs(left-right)
    return best

def shanon_fano(freq,names):
    freq = tuple(sorted(tuple(arr_namer(freq,names)), reverse=True))
    freq = sorted(freq, key= lambda x: (-x[0], x[1]))
    graph = dict()
    number = dict()
    arr = list()
    arr.append(freq)
    names = [i[1] for i in freq]
    #print("\nFrecuencias ordenadas:\n")
    #for f in freq:
        #print('[{}] - {}'.format(f[1],f[0]))
    #print("")
    start = str()
    for group in arr:
        for element in group:
            start += element[1]
    while arr:
        temp_arr = list()
        for group in arr:
            name = str()
            for element in group:
                name += element[1]
            graph[name] = []
            pair = best_pair(group)
            

            i = 0
            for each in pair:
                
                if isinstance(each[0], float) or isinstance(each[0], Fraction):
                    graph[name].append(each[1])
                    number[each[1]] = i
                    graph[each[1]] = []
                else:
                    temp_arr.append(each)
                    name2 = str()
                    for element in each:
                        name2 += element[1]
                    graph[name].append(name2)
                    number[name2] = i
                i += 1
        arr = list(temp_arr)
    return [graph, number, names, start, freq]

def find_path(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    if start not in graph:
        return None
    for node in graph[start]:
        if node not in path:
            newpath = find_path(graph, node, end, path)
            if newpath:
                return newpath
    return None

def decoder(graph, start, names, codes, named_arr):
##    print("Nodos:\n")
##    for k, v in graph.items():
##        if v == []:
##            pass
##        else:
##            print(k,'-',v)
    print("\nTablilla de codificación (Shanon-Fano)\n")
    ls, freq_values = dict(), dict()
    for value in named_arr:
        freq_values[value[1]] = value[0]
        
    tablilla = {}
    for name in names:
        print("[{}] - ".format(name), end='')
        path = find_path(graph, start, name)
        path = path[1:]
        code = []
        if len(path) not in ls:
            ls[len(path)] = []
            ls[len(path)].append(name)
        else:
            ls[len(path)].append(name)
        for n in path:
            code.append(codes[n])
        print(code)
        tablilla['{}'.format(name)] = code
    return tablilla
    print("\nRadio de compresión\n")
    code_length = 0
    for k, v in ls.items():
        s = 0
        for x in v:
            s += freq_values[x]
        code_length += (k*s)
    print("Ls = {} bits/símbolo".format(round(float(code_length),4)))
    rc = round(float(8/code_length),4)
    print("Rc = {}".format(rc))

def main():
    data = user_input()
    freq = data[0]
    names = data[1]
    string = data[2]
    data = shanon_fano(freq,names)
    codes = decoder(data[0],data[3],data[2],data[1],data[4])
    return codes, string
    #input("\nPresione [Enter] para salir.")

def frequency_input():
    print("\nIngrese la cantidad de frecuencias deseadas.")
    while True:
        try:
            qty = int(input("\nSeleccion: "))
            if qty <= 1:
                print("[Error] El minimo de frecuencias necesarias es 2.")
            else:
                break
        except Exception:
            print("[Error] Ingrese un valor numerico entero mayor a 1.")
    freq = []
    limit = 1
    current = 0
    for x in range(qty):
        while True:
            try:
                fi = float(input("\nFrecuencia {}: ".format(x+1)))
                if fi <= 0 or fi >= 1:
                    print("[Error] El valor de la frecuencia debe ser mayor a 0 y menor a 1")
                else:
                    temp_sum = current
                    current += Decimal("{}".format(fi))
                    if current >= limit and x+1 != qty:
                        print("[Error] El valor de la frecuencia provoca que el total se exceda o alcance el limite")
                        print("[Mensaje] Ingrese un valor menor a {}".format(1-temp_sum))
                        current = temp_sum
                    elif current > limit and x+1 == qty:
                        print("[Error] El valor de la frecuencia provoca que el total se exceda del limite")
                        print("[Mensaje] El unico valor posible es: {}".format(1-temp_sum))
                        current = temp_sum
                    elif current < limit and x+1 == qty:
                        print("[Error] El valor de la frecuencia final no alcanza el limite")
                        print("[Mensaje] El unico valor posible es: {}".format(1-temp_sum))
                        current = temp_sum
                    else:
                        #freq.append(Fraction('{}'.format(fi)))
                        freq.append(fi)
                        break
            except ValueError:
                print("[Error] Ingrese un valor numerico entre 0 y 1.")
    return freq

def string_frequencies(string):
    arr = list(string)
    freqs = dict()
    names = list()
    probs = list()
    for element in string:
        if element in freqs:
            freqs[element] += 1
        else:
            freqs[element] = 1
            
    for name, times in freqs.items():
        names.append(name)
        probs.append(Fraction('{}/{}'.format(times,len(arr))))

    return [probs, names, string]

def string_input():
    print("\nOpciones:\n")
    print("1. Ingresar el string manualmente.\n2. Obtener el string del archivo de texto.")
    while True:
        try:
            choice = int(input("\nSeleccion [1,2]: "))
            if choice < 1 or choice > 2:
                raise Exception
            else:
                break
        except Exception:
            print("[Error] Ingrese una de las opciones disponibles (1,2)")
    if choice == 1:
        string = input("Ingrese el string: ")
    elif choice == 2:
        string = ''
        with open("data.txt","r",encoding='utf-8-sig') as data:
            f = data.readlines()
            for line in f:
                for x in line.strip():
                    string += x
    else:
        print("Error inesperado.")
    return string_frequencies(string)

def seed(initVal):
    global rand
    rand = initVal

def seudo_random():
    a = int(time.time())
    a = 8*a - 3
    c = 0
    m = 32747
    global rand
    rand = (a*(rand + c)) % m
    rand = rand/m
    return rand

seed(7)

def sum_equals_one(arr):
    arr.append(0)
    arr.append(1)
    arr = sorted(arr)
    new_arr = list()
    for i, x in enumerate(arr):
        if i == 0:
            pass
        new_element = abs(Decimal('{}'.format(arr[i])) - Decimal('{}'.format(arr[i-1])))
        new_element = float(new_element)
        if new_element == 1:
            pass
        else:
            new_arr.append(new_element)
    return new_arr

def random_frequencies():
    print("\nIngrese la cantidad de frecuencias deseadas.")
    while True:
        try:
            qty = int(input("\nSeleccion: "))
            if qty <= 1:
                print("[Error] El minimo de frecuencias necesarias es 2.")
            else:
                break
        except Exception:
            print("[Error] Ingrese un valor numerico entero mayor a 1.")
    arr = list()
    for i in range(qty-1):
        while True:
            x = round(seudo_random(),2)
            if x > 0 and x < 1 and x not in arr:
                arr.append(x)
                break
    final_arr = sum_equals_one(arr)
    return final_arr
                    
def user_input():
    choice = 2
    if choice == 1:
        return [frequency_input(),list(string.ascii_lowercase)]
    elif choice == 2:
        data = string_input()
        return [data[0],data[1],data[2]] # Pendiente los aleatorios.
    elif choice == 3:
        return [random_frequencies(), list(string.ascii_lowercase)]
    else:
        print("Error inesperado.")

#if __name__ == '__main__':
    #print(main())
    
        


            
            
    
    

















    
    
    
