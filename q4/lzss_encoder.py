#Name   : Calum Lim Sheng En
#ID     : 27372537
#Title  : FIT3155 - Assignment 2: Q4 - Encoder
#Date   : 21/10/2018

import sys

#function implementation to convert a dec value into binary form
#Referenced from: https://www.youtube.com/watch?v=XdZqk8BXPwg
def convert_binary(n):
    binary_str = ""
    while (n>=1):
        if n%2==0:
            binary_str+="0"
        else:
            binary_str+="1"
        n//=2
    return binary_str[::-1]

#function implementation to convert a given value into elias encoding
def elias_encoding(n):
    encoded_binary = ""
    binary = convert_binary(n)
    encoded_binary+=binary
    k = len(binary)-1

    while (k>=1):
        front_binary = convert_binary(k)
        front_binary = "0"+front_binary[1:len(front_binary)]
        encoded_binary = front_binary+encoded_binary
        k = len(front_binary)-1
    return encoded_binary

#function implementation to encode a string into LZSS format
def LZSS(string, window, b_size):
    buffer = ""
    encoded_arr = []
    k = 0
    while (k<len(string)):
        #dictionary size is lesser than 3
        if k<3:
            buffer = string[k]
            encoded_arr.append([1, buffer])
        else:
            #dictionary is 3 or more
            pointer,counter, match_count = k-1,0,[]
            while pointer>=0 and counter<=window:
                match_counter = 0
                for i in range(b_size):
                    if string[pointer]!=string[k]:
                        break
                    if k+i<=len(string)-1:
                        if string[pointer+i]==string[k+i]:
                            match_counter+=1
                        else:
                            break
                match_count.append([match_counter, k-pointer])
                if match_counter==b_size:   #if the number of matches is same as the buffer size, break
                    break
                pointer-=1
                counter+=1
            max_match, offset = match_count[0][0], match_count[0][1]
            #find the maximum matches in a given window, and get its position
            for i in range(1,len(match_count)):
                if match_count[i][0]>max_match:
                    max_match, offset = match_count[i][0], match_count[i][1]
            if max_match>=3:
                k+=max_match-1
                encoded_arr.append([0, offset, max_match])
            else:
                encoded_arr.append([1, string[k]])
        k+=1
    return encoded_arr  #return an array in LZSS format

#function implementation to convert LZSS format values into binary values with 8 bits
def encoder(arr):
    encoded_arr = []
    k = len(arr)
    for i in range(k):
        if len(arr[i])==2:  #in the format of eg. (1,"a")
            encoded_arr.append(str(arr[i][0])+"0"+convert_binary(ord(arr[i][1])))
        else:   #in the format of eg. (0,3,4)
            encoded_arr.append(str(arr[i][0])+elias_encoding(arr[i][1])+elias_encoding(arr[i][2]))
    return "".join(encoded_arr) #return a string of the encoded binary values

#function implementation to write the results into a text file
def writeFile(string):
    f = open("output_lzss_encoder.txt", "w+")
    f.write(string)
    f.close()

#function implementation to read from a text file
def openFile(filename, w, b):
    string = ""
    f = open(filename, "r+")
    for line in f:
        string+=line
    writeFile(encoder(LZSS(string,w,b)))
    f.close()

#main driver for this program
if __name__ == "__main__":
    filename = sys.argv[1]
    wInp = sys.argv[2]
    bInp = sys.argv[3]

    openFile(filename, int(wInp), int(bInp))
