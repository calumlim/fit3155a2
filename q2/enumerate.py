#Name   : Calum Lim Sheng En
#ID     : 27372537
#Title  : FIT3155 - Assignment 2: Q2
#Date   : 13/10/2018

import sys

class BinaryEnumeration:
    def __init__(self, n):
        self.n, self.final_arr = n, []
        for i in range(self.n+1):
            if i==0:
                self.final_arr.append(["1"])
            else:
                self.final_arr.append([])   #initiating the first value
        self.enumerate(self.final_arr[0][0][0], [0,1], 0)   #enumeration function
        self.writeFile(self.final_arr)  #write to an output txt file

    #recursive function to loop replace the positions of 1s with "011",
    #maximum traverse through each string is k//2
    def enumerate(self, prev_string, pos_arr, counter):
        if counter==self.n:
            return
        counter+=1
        for i in range(pos_arr[0], pos_arr[1]):
            concat_str = prev_string[0:i]+"011"+prev_string[i+1:len(prev_string)]
            self.final_arr[counter].append(concat_str)
            #recursive call for next BST
            self.enumerate(concat_str, [i+1, len(concat_str)], counter)

    #function implementation to write to txt file
    def writeFile(self, arr):
        f,counter = open("output_enumerate.txt", "w+"), 1
        for i in range(len(arr)):
            for j in range(len(arr[i])):
                if i==len(arr)-1 and j==len(arr[i])-1:
                    f.write(str(counter)+ " "+ arr[i][j])
                else:
                    f.write(str(counter)+ " "+ arr[i][j]+"\n")
                counter+=1
        f.close()

#main driver for the program
if __name__ == "__main__":
    N = sys.argv[1]
    q = BinaryEnumeration(int(N))
