import numpy as np

rpm_to_send = np.int64(65536)

header_data = (rpm_to_send.item()).to_bytes(2, 'big')
print(header_data)