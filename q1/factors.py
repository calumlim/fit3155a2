#Name   : Calum Lim Sheng En
#ID     : 27372537
#Title  : FIT3155 - Assignment 2: Q1
#Date   : 21/10/2018

import sys
import random

class PrimeFactors:
    def __init__(self, n):
        self.n = n
        self.final_arr = []
        for i in range(self.n, 1, -1):  #iteration to check if i is prime value or not
            if i>self.n-100:
                if self.is_large_prime(i)==True and len(self.final_arr)!=100:
                    self.findPrimeFactors(i+1, [], 0, 0, i+1)
            else:
                if self.is_small_prime(i)==True and len(self.final_arr)!=100:
                    self.findPrimeFactors(i+1, [], 0, 0, i+1)
        self.writeFile(self.final_arr)

    #Naive implementation of primality testing
    def is_small_prime(self, n):
        if n<=1:
            return False
        elif n<= 3:
            return True
        elif n%2==0 or n%3==0:
            return False
        i = 5
        while i*i<=n:
            if n%i==0 or n%(i+2)==0:
                return False
            i+=6
        return True

    #Miller-Rabin implementation for primality testing with a constant k=64
    #Referenced from: https://gist.github.com/Ayrx/5884790
    def is_large_prime(self, n, k=64):
        #First few cases
        if n<=1:
            return False
        if n==2 or n==3:
            return True
        if (n%2)==0:
            return False    #if n is divisible by 2 return false
        initial = 0
        counter = n - 1
        while counter%2==0:
            initial+=1
            counter//=2
        for i in range(k):
            random_no = random.randrange(2,n-1)     #initiate a random number
            power = pow(random_no, counter, n)
            if power==1 or power==n-1:
                continue
            for i in range(initial-1):
                power = pow(power, 2, n)
                if power==n-1:
                    break
            else:
                return False    #return false if it isn't a prime number
        return True     #return true if its a prime number

    #Recursive function implementation to compute all the prime factors for a given n value
    #will return an array containing the composite number together with its prime factors
    def findPrimeFactors(self, n, arr, counter, prev_prime, composite_no):
        i = 2
        if n<=1:
            prime_factors = "   "
            for i in range(len(arr)):
                prime_factors+=str(arr[i][0])+"^"
                if i!=len(arr)-1:
                    prime_factors+=str(arr[i][1])+" X "
                else:
                    prime_factors+=str(arr[i][1])
            self.final_arr.append([composite_no, prime_factors])
            return arr

        #keep incrementing to test if the next value is a prime or not
        #if prime, check if divisible
        while (True):
            prime_bool = None
            if i>self.n-(self.n*0.1):
                prime_bool = self.is_large_prime(i)
            else:
                prime_bool = self.is_small_prime(i)
            if prime_bool and n%i==0:
                if i!=prev_prime:
                    arr.append([i, 1])
                    counter+=1
                if arr!=[]:
                    if i==prev_prime:
                        arr[counter-1][1]+=1
                return self.findPrimeFactors(int(n/i), arr, counter, i, composite_no)
            i+=1

    #Function implementation to write all prime factors to a file
    def writeFile(self, arr):
        f = open("output_factors.txt","w+")
        for i in range(len(arr)-1,-1,-1):
            if i==0:
                f.write(str(arr[i][0])+"    "+arr[i][1])
            else:
                f.write(str(arr[i][0])+"    "+arr[i][1]+"\n")
        f.close()

#main driver for the program
if __name__ == "__main__":
    N = sys.argv[1]
    q = PrimeFactors(int(N))
