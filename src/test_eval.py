import numpy as np
import pandas as pd



# cmd_file_path = input("Input command file path: ")
# print("Reading Command file...")
# frame = pd.read_csv(cmd_file_path)
# print("Frame:\n\n", frame)
# cmd_array = frame.to_numpy()
# print("Numpy array:\n\n", cmd_array)
# print(type(cmd_array[3, 0]))
# print(type(cmd_array[3,1]))
# return cmd_array



a1 = np.array([[1,2],[3,4],[5,6],[7,8],[9,10]])
print("a1:\n", a1)

a2 = np.zeros((10,2))
print("a2:\n", a2)

a3 = np.array([[1+2,2],[3,4],[5,6],[7,8],[9,10]])
print("a3:\n", a3)

f1 = pd.DataFrame([[1,2],[3,4],[5,6],[7,8],[9,10]])
print("f1:\n", f1)

f2 = pd.DataFrame([[1+2,2],[3,4],[5,6],[7,8],[9,10]])
print("f2:\n", f2)

f3 = pd.read_csv("/home/colton/Documents/GitHub/JetCat_Comms/throttle_curves/throttle_curves_rpm/2023-02-16.txt")
print("f3:\n", f3)

f4 = f3.applymap(lambda x: eval(x) if isinstance(x, str) else x    )
print("f4:\n", f4)

a4 = f4.to_numpy()
print("a4:\n", a4)