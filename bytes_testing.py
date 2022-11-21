import numpy as np
import cw_helper2
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

bytes4 = bytes3[1:5]
print("Bytes4:\n",bytes4)




# packet = bytes1[1:5]
# print(packet)
# print(type(packet))
# print(len(packet))
# print(packet[len(packet)-1])

# array1 = np.zeros((10,1))
# array2 = np.array([[125,2],[241,222]])
# print(array1)
# print(array2)

bytes1 = b'\x7D\x5D\x05\xF3\xEE\x7D\x5D\x00\x02\xFF\x7D\x5E\x00\x00\x00\x00\x00'
unstuff = cw_helper2.byte_unstuffing(bytes1)
print("unstuff:\n",unstuff, '\n\n')
print("len(unstuff):\n", len(unstuff), "\n\n")

tuple1 = (1,2,3,4,5)
print(tuple1)
print(tuple1[2])
print(__name__)

