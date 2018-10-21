#Name   : Calum Lim Sheng En
#ID     : 27372537
#Title  : FIT3155 - Assignment 2: Q3
#Date   : 21/10/2018

import sys

#function implementation to calculate the number of trees given k internal
#nodes by utilizing the binomial function defined
#Referenced from: https://www.geeksforgeeks.org/program-nth-catalan-number/
def catalan(k):
    result = calculate_binomial(2*k, k)
    return result//(k + 1)

#function implementation to calculate the binomial value for a given n and k
#in linear time
def calculate_binomial(n, k):
    if k>n-k:
        k=n-k
    result = 1
    for i in range(k):
        result*=(n-i)
        result//=(i+1)
    return result

#function implementation to calculate the factorial of a given value
def factorial(n):
    if n == 0:
        return 1
    else:
        return n*factorial(n-1)

#function implementation to calculate the catalan triangle formula
def catalan_triangle(n, k):
    topleft = factorial(n+k)
    topright = n-k+1
    bottom = factorial(k)*factorial(n+1)
    return (topleft*topright)//bottom

#function implementation to split a single line of binary string to multiple bitstrings
#for further computation
def split_bitstring(bitstring):
    start_ind, find_pat, countOne, countZero, i, arr = 0, 0, 0, 0, 0, []
    while i<len(bitstring):
        if bitstring[i]=="0":
            countZero+=1
        else:
            #case when "1" is at the start of the string
            if i==0 and bitstring[i]=="1":
                arr.append([0,1])
                start_ind+=1
            else:
                countOne+=1
        if bitstring[i:i+3]=="011":
            find_pat+=1
        #properties of an enumeration bitstring include:
            #bitstring's length must be odd
            #there must be "011" in it unless for the case of "1"
            #number of ones must exceed number of 0s
        if (countZero+countOne)%2!=0 and find_pat>=1 and countOne>countZero:
            arr.append([start_ind, i+1])
            if i+1<len(bitstring) and bitstring[i+1]=="1":
                arr.append([i+1,i+2])
                i+=1
                start_ind = i+1
            else:
                start_ind = i+1
            countZero, countOne, find_pat = 0,0,0
        i+=1
    return arr  #return an array consisting of all the bitstrings

#function implementation to find the number of trees before the given bitstring
#this function utilizes the properties of Dyck words together with computations
#derived from the Catalan Triangle
def find_rank(bitstring):
    n, rank, query_pos, one_position, no_of_ones, no_of_zeros, prefix_arr,end_pos= 0,0,0,[],0,0,[],0

    #searching for no. of internal nodes, position of query string & positions of 1s
    k = len(bitstring)
    for i in range(k-1,-1,-1):
        if bitstring[i]=="0":
            end_pos = i+1
            break
    #return if "011" or "1" case
    if end_pos<=2:
        return end_pos+1

    #when all 0s are in the front and all 1s are in the back
    if end_pos==(len(bitstring)//2):
        query_pos=end_pos+1

    #obtaining the number of internal nodes, together with the position of query string eg. "0001"
    for i in range(0,end_pos):
        if bitstring[i]=="0":
            n+=1
        elif bitstring[i]=="1":
            if query_pos == 0:
                query_pos = i
            else:
                one_position.append(i)
    #creating first group of prefixes
    for i in range(n-query_pos):
        rank+=catalan_triangle(n-1, i)

    #creating the second group of prefixes
    for i in range(len(one_position)):
        prefix_str = bitstring[query_pos+1:one_position[i]]+"0"
        no_of_zeros+=query_pos
        for j in range(len(prefix_str)):
            if prefix_str[j]=="0":
                no_of_zeros+=1
            else:
                no_of_ones+=1
        rank+=catalan_triangle(n-i-1, (n-i)-(no_of_zeros-no_of_ones))
        no_of_zeros, no_of_ones = 0, 0

    #sum of the previous n internal node trees
    catalan_sum = 0
    for i in range(n):
        catalan_sum+=catalan(i)
    return catalan_sum+rank+1

#function implementation to generate the values for each bitstring
def sum_trees(bitstring):
    tree_arr = []
    bitstring_arr = split_bitstring(bitstring)  #splitting the bitstring from a single line
    for i in range(len(bitstring_arr)):
        #finding the rank for each bitstring
        tree_arr.append(find_rank(bitstring[bitstring_arr[i][0]:bitstring_arr[i][1]]))
    return tree_arr

#function implementation to write array elements into an output txt file
def writeFile(arr):
    f = open("output_intseqdecode.txt", "w+")
    intseq = ""
    for i in range(len(arr)):
        if i!=len(arr)-1:
            intseq+=str(arr[i])+","
        else:
            intseq+=str(arr[i])
    f.write(intseq)
    f.close()
    return intseq

#function to open a txt file based on its filename
def openFile(filename):
    bitstring = ""
    f = open(filename, "r+")
    for line in f:
        bitstring+=line
    final_str = writeFile(sum_trees(bitstring))
    return final_str

#main driver for this program, takes in a txt filename as its input
if __name__ == "__main__":
    filename = sys.argv[1]
    openFile(filename)
