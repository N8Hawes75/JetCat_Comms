import numpy as np

bytes1 = b'\xe6\x02\x0F\x00\x09\x04\xc9\x0b\x00\x12\xc0'
bytes2 = b'\x86\x99\x44\x55'
bytes3 = bytes1 + bytes2
print("Bytes1:\n")
print(bytes1)
print(type(bytes1))
print(bytes1[1])
print("Bytes3:\n")
print(bytes3)
print(type(bytes3))
print(bytes3[8])




packet = bytes1[1:5]
print(packet)
print(type(packet))
print(len(packet))
print(packet[len(packet)-1])

array1 = np.zeros((10,1))
array2 = np.array([[125,2],[241,222]])
print(array1)
print(array2)