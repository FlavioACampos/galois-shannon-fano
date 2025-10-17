# Encoding: UTF-8-sig
# Python 3.7.0
# Windows 10

from numpy import poly1d as poly
from shanon_fano import main as coding
import codecs
import csv
import os

def polynomial_form(binary_string):
    SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
    binary_string = binary_string.strip()
    k = len(binary_string)-1
    if binary_string == '0':
        return None
    
    polynomial = []
    for k, x in zip(range(k, -1, -1),binary_string):
        if x == '0':
            pass
        else:
            if k == 0:
                polynomial.append('1')
            elif k == 1:
                polynomial.append('x')
            else:
                exp = '{}'.format(k).translate(SUP)
                polynomial.append('x{}'.format(exp))
                
    return (' + '.join(polynomial))

def filler(bin_list, bits):
    limit = bits - len(bin_list)
    if limit == 0:
        return ''.join(bin_list)
    
    if limit < 0:
        print("\nError: {}".format(bin_list))
        return None
    
    else:
        for x in range(limit):
            bin_list.insert(0, '0')
            
        return ''.join(bin_list)

def first_polynomials(bits):
    a = {32:[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
         31:[1,0,0,1],
         30:[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
         29:[1,0,1],
         28:[1,0,0,1],
         27:[1,0,0,1,1,1],
         26:[1,0,0,0,1,1,1],
         25:[1,0,0,1],
         24:[1,0,0,0,0,1,1,1],
         23:[1,0,0,0,0,1],
         22:[1,1],
         21:[1,0,1],
         20:[1,0,0,1],
         19:[1,0,0,1,1,1],
         18:[1,1,1,1,1,1],
         17:[1,0,0,1],
         16:[1,1,1,1,0,1,1,1,0,1],
         15:[1,1],
         14:[1,0,1,0,0,0,0,1,1],
         13:[1,1,0,1,1],
         12:[1,0,1,0,0,1,1],
         11:[1,0,1],
         10:[1,0,0,1],
         9: [1,0,0,0,1],
         8: [1,1,1,0,1],
         7: [1,0,0,1],
         6: [1,1],
         5: [1,0,1],
         4: [1,1],
         3: [1,1],
         2: [1,1],
         1: [1],
         }
    
    return a[bits]

def primitive_polynomials(bits):
    a = {32:'100000000010000000000000000000111',
         31:'10000000000000000000000000001001',
         30:'1000000100000000000000000000111',
         29:'100000000000000000000000000101',
         28:'10000000000000000000000001001',
         27:'1000000000000000000000100111',
         26:'100000000000000000001000111',
         25:'10000000000000000000001001',
         24:'1000000000000000010000111',
         23:'100000000000000000100001',
         22:'10000000000000000000011',
         21:'1000000000000000000101',
         20:'100000000000000001001',
         19:'10000000000000100111',
         18:'1000000000000111111',
         17:'100000000000001001',
         16:'10000001111011101',
         15:'1000000000000011',
         14:'100000101000011',
         13:'10000000011011',
         12:'1000001010011',
         11:'100000000101',
         10:'10000001001',
         9: '1000010001',
         8: '100011101',
         7: '10001001',
         6: '1000011',
         5: '100101',
         4: '10011',
         3: '1011',
         2: '111',
         1: '11',
         }
    return a[bits]

def field_constructor(bits, file):
    csv_writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)
    alpha = poly([1,0])
    primitive = primitive_polynomials(bits)
    first_poly = first_polynomials(bits)
    
    main_row = []
    row2 = []
    i = bits
    main_row.append('Index_form')
    
    row2.append('0')
    for x in range(bits):
        i -= 1
        main_row.append('x{}'.format(i))
        row2.append('0') 
        
    main_row.append('binary')
    main_row.append('decimal')
    main_row.append('polynomial_form')
        
    csv_writer.writerow(main_row)
        
    row2.append('0'*bits+'₂')
    row2.append('0')
    row2.append('0')

    csv_writer.writerow(row2)
    SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
    for b in range(int(2**bits)):
        
        row = []
        if b < bits:
            check = 2**b
            binary = list(bin(check))
            binary = filler(binary[2:], bits)
            
            row.append(('α{}'.format(b)).translate(SUP))
            for x in binary:
                row.append('{}'.format(x))
                
            row.append("{}₂".format(binary))
            row.append('{}'.format(int('0b'+binary, 2)))
            row.append('{}'.format(polynomial_form(binary)))
            csv_writer.writerow(row)
            
            #print(binary,'α^{}'.format(b), int('0b'+binary, 2))
            
        elif b == bits:
            check = first_poly
            binary = [str(i) for i in check]
            binary = filler(binary, bits)

            row.append(('α{}'.format(b)).translate(SUP))
            for x in binary:
                row.append('{}'.format(x))
                
            row.append("{}₂".format(binary))
            row.append('{}'.format(int('0b'+binary, 2)))
            row.append('{}'.format(polynomial_form(binary)))
            csv_writer.writerow(row)
            
            #print(binary,'α^{}'.format(b), int('0b'+binary, 2))
            current = int('0b'+binary, 2)
        
        else:
            current = current * 2
            binary = list(bin(current))
            if len(binary[2:]) > bits:
                current = current ^ int(primitive, 2)
                binary = list(bin(current))
                binary = filler(binary[2:], bits)
                #print(binary,'α^{}'.format(b), int('0b'+binary, 2))
                
            else:
                binary = filler(binary[2:], bits)
                #print(binary,'α^{}'.format(b), int('0b'+binary, 2))

            row.append(('α{}'.format(b)).translate(SUP))
            for x in binary:
                row.append('{}'.format(x))
                
            row.append("{}₂".format(binary))
            row.append('{}'.format(int('0b'+binary, 2)))
            row.append('{}'.format(polynomial_form(binary)))
            csv_writer.writerow(row)

def string_to_binary(string='ok'):
    string = string.encode('utf-8')
    bytes_as_bits = ' '.join(format(x, 'b') for x in bytearray(string))
    #print("String original: {}".format(string.decode('utf-8')))
    #print(bytes_as_bits)
    return bytes_as_bits

def binary_to_string(binary):
    binary = binary.split(" ")
    string = ''
    for x in binary:
        string += chr(int(x,2))
    #print("String recibido: {}".format(string))
    #print(string_to_binary(string))
    return string

def edit_bit(binary):
    from random import randrange
    binary = list(binary)
    bit = randrange(0, len(binary))
    if binary[bit] == '0':
        binary[bit] = '1'
    else:
        binary[bit] = '0'
    return ''.join(binary)

def binary_errors(binary):
    from random import randrange, sample
    binary = binary.split(" ")
    if len(binary) == 1 or len(binary) == 2:
        n_errors = 1
    else:
        n_errors = randrange(1,int(len(binary)/2))
    errors = sample(range(0, len(binary)),n_errors)
    for x in errors:
        binary[x] = edit_bit(binary[x])
    return ' '.join(binary)
    
def main(string, table):
    fields = [len(y) for x, y in table.items()]
    bits_list = tuple(set(fields))

    print("\nGeneracion de los Campos de Galois necesarios ({}).\n".format(len(bits_list)))
    for bits in bits_list:
        file = open('campos generados/GF(2^{}).csv'.format(bits),'w',encoding='utf-8-sig', newline='')
        field_constructor(bits, file)
        file.close()
        print("Generando: [G = 2^{}]".format(bits))
        #os.startfile('GF.csv')

if __name__ == '__main__':
    data = coding()
    table = data[0]
    string = data[1]
    main(string, table)
    print("\nListo\n")
    input("Presione [Enter] para salir.")
            
