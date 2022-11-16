# -*- coding: utf-8 -*-


print('\n Quantum Adder')
print('----------------')

from qiskit import QuantumRegister
from qiskit import ClassicalRegister
from qiskit import QuantumCircuit, execute,IBMQ
import matplotlib.pyplot as plt

IBMQ.enable_account('4e41e668b8f6836bd6b38a94aa26091aa7ee3968f1114c23c38a8ab74f2889c3f799444432ff05e9c30e299330d94669bcfc3dce43082717133c51a29d19accf')
provider = IBMQ.get_provider(hub='ibm-q')
#backend = provider.get_backend('ibmq_qasm_simulator')
backend = provider.get_backend('ibmq_manila')
#A function to translate base-ten into binary#
def getbinary(x):
    x = int(x)
    x = format(x, "b")
    return x

#Define the inputs#
A = input("Enter a number less than 126: ")
A =  getbinary(A)
B = input("Enter another number less than 126: ")
B = getbinary(B)
print("A=", A)
print("B=", B)
#Check how many bits (n) we will need
lA = len(A)
lB = len(B)

if lA > lB:
    n = lA
else:
    n= lB
    
#Define the registers for the inputs#
a = QuantumRegister(n) #A
b = QuantumRegister(n+1) #B
c = QuantumRegister(n) #Carry
cr = ClassicalRegister(n+1) #Classical output
qc = QuantumCircuit(a, b, c, cr)

#Write the input into the qubits
for i in range(lA):
    if A[i] == "1":
       qc.x( a[lA - (i+1)] )
for i in range(lB):
   if B[i] == "1":
      qc.x( b[lB - (i+1)] ) 
      
#Construct the carry gate
for i in range(n-1):
    qc.ccx(a[i], b[i], c[i+1])
    qc.cx(a[i], b[i])
    qc.ccx(c[i], b[i], c[i+1])
    
qc.ccx(a[n-1], b[n-1], b[n])
qc.cx(a[n-1], b[n-1])
qc.ccx(c[n-1], b[n-1], b[n])

#Implement the sum gate#
for i in range(n-1):
    #First we need to revert the qubits back to their orignal state#
    qc.ccx(a[(n-2)-i], b[(n-2)-i], c[(n-1)-i])
    qc.cx(a[(n-2)-i], b[(n-2)-i])
    qc.ccx(c[(n-2)-i], b[(n-2)-i], c[(n-1)-i])
    #Sum operation#
    qc.cx(c[(n-2)-i], b[(n-2)-i])
    qc.cx(a[(n-2)-i], b[(n-2)-i])
    
#Transform back into classical bits
qc.measure(b,cr)
job = execute(qc, backend, shots=10)
job_result = job.result().get_counts()
names = list(job_result.keys())
values = list(job_result.values())
plt.bar(range(len(job_result)), values, tick_label=names)
plt.show()
print(job_result)
IBMQ.disable_account()