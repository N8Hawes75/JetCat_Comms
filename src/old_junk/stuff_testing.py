import throttle_help



h1 = b"\x01\x01\x02\x06\x02'\x10\r\xee"
s_h1 = throttle_help.stuff_header(h1)

h2 = b"\x01\x01\x7E\x06\x02'\x10\r\xee"
s_h2 = throttle_help.stuff_header(h2)

h3 = b"\x01\x01\x7D\x06\x02'\x10\r\xee"
s_h3 = throttle_help.stuff_header(h3)


h3 = b"\x01\x01\x7D\x06\x02'\x10\x7E\xee"
s_h3 = throttle_help.stuff_header(h3)


print("\n\nh4:")
h4 = b'\x01\x01\x02\x01\x02\x0f\xa0\x02\x7D'
h4_array = bytearray(h4)

s_h4 = throttle_help.stuff_header(h4)

# Test if it cycles through the entire array now with multiple stuffing
print("\n\n\nh5:")
h5 = b'\x01\x01\x7E\x01\x02\x0f\xa0\x02\x7D'
print(h5[8])
s_h5 = throttle_help.stuff_header(h5)

print(s_h5)

# Seems everything works