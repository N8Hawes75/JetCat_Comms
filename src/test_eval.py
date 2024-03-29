import numpy as np
import pandas as pd
import os


# cmd_file_path = input("Input command file path: ")
# print("Reading Command file...")
# frame = pd.read_csv(cmd_file_path)
# print("Frame:\n\n", frame)
# cmd_array = frame.to_numpy()
# print("Numpy array:\n\n", cmd_array)
# print(type(cmd_array[3, 0]))
# print(type(cmd_array[3,1]))
# return cmd_array

def modify_value(value):
    # This function will be applied to each value in the csv file. So check if
    # a % is there, and change it to a RPM command instead of % command.
    # also evaluate expressions so that 25+60 is just 85


    if isinstance(value, str):

        if "%" in value:
            value = float(value.strip('%'))
            value = 700*value + 34000 # Map 0% to 34000rpm, 100% to 104000rpm
            value = str(value)

        if ("+" in value) or ("(" in value):
            value = eval(value)


    return value

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

f4 = f3.applymap(modify_value)
print("f4:\n", f4)

a4 = f4.to_numpy()
print("a4:\n", a4)

path = './folder1/folder2/file.txt'
second_to_last = os.path.sep.join(os.path.abspath(path).split(os.path.sep)[-2:])
second_to_last = os.path.sep + second_to_last

print(second_to_last) # Outputs '/folder2/file.txt'

def save_to_t7(data_filename, log_filename):
    print("Copy files to T7")
    full_path_to_T7 = "/media/colton/JetCat_Data"
    test = os.path.basename(os.path.normpath('/folderA/folderB/folderC/folderD/'))
    shutil.copy2(data_filename, os.join(full_path_to_T7, ) )

