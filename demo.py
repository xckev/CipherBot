from Pyfhel import Pyfhel
import numpy as np
import requests
import os

HE = Pyfhel()

def enc(votes):
    HE.contextGen(scheme='bfv', n=2**14, t_bits=20)
    HE.keyGen()

    encvotes = []
    for elem in votes:
        i = np.array([elem], dtype=np.int64)
        ctxt = HE.encryptInt(i)
        encvotes.append(ctxt)
    
    return encvotes

def combine(encvotes):
    ctxtSum = encvotes[0]
    for i in range(1, len(encvotes)):
        ctxtSum += encvotes[i]
    return HE.decryptInt(ctxtSum)

def mix(votes):
    sz = len(votes)
    perm = np.random.permutation(sz)
    m = []
    for elem in perm:
        m.append(votes[elem])
    return m

v = [1, 1, -1, 1, -1, 1]
mixed = mix(v)
enced = enc(mixed)
print(combine(enced)[0])