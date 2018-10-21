#Name   : Calum Lim Sheng En
#ID     : 27372537
#Title  : FIT3155 - Assignment 2: Q4 - Decoder
#Date   : 21/10/2018

import sys

#function implementation to convert binary back to decimal using base 2
def binary_to_decimal(binary):
    dec = 0
    for i in range(len(binary)-1,-1,-1):
        if binary[i]=="1":
            dec+=pow(2, abs(i-len(binary)+1))
    return dec

#function implementation to decode previously encoded elias encoding back to its original number
def elias_decoder(binary, pointer):
    readlen = 1
    pos = 0
    component = binary[pointer:pointer+pos+readlen]
    while component[0]!="1":    #execute while the leftmost value isn't 1
        component = component[1:]
        component = "1" + component
        pos = readlen + pos
        readlen = binary_to_decimal(component) + 1
        component = binary[pointer+pos:pointer+pos+readlen]
    return [binary_to_decimal(component), pointer+pos+readlen]  #return the value, together with the next position in the string

#function implementation to decode previously encoded LZSS binary strings
def LZSS_decoder(binary):
    k = 0
    decoded_str = ""
    while (k<len(binary)):
        #segregating the binary values
        if binary[k]=="1":  #case of eg. (1,"a")
            query_str = binary[k+1:k+9]
            decoded_char = chr(binary_to_decimal(query_str))
            decoded_str+=decoded_char
            k+=9
        else:   #case of eg. (0,3,4)
            #do elias decoding twice for the offset and the length
            first_elias = elias_decoder(binary, k+1)
            k=first_elias[-1]
            second_elias = elias_decoder(binary, k)
            k=second_elias[-1]
            offset = [first_elias[0], second_elias[0]]

            #adding the characters based on the offset and length
            start_ind = len(decoded_str)-offset[0]
            for i in range(offset[1]):
                decoded_str+=decoded_str[start_ind]
                start_ind+=1
    return decoded_str  #return the entire decoded string

#function implementation of writing a string into a text file
def writeFile(string):
    f = open("output_lzss_decoder.txt", "w+")
    f.write(string)
    f.close()

#function implementation of reading a file based on its filename then decoding it
def openFile(filename):
    string = ""
    f = open(filename, "r+")
    for line in f:
        string+=line
    writeFile(LZSS_decoder(string))
    f.close()

#main driver for this program
if __name__ == "__main__":
    filename = sys.argv[1]
    wInp = sys.argv[2]
    bInp = sys.argv[3]

    openFile(filename)
