"""
Create a _crc.c library so that we can calculate crc16 checksums.
"""

from cffi import FFI


ffibuilder = FFI()
ffibuilder.cdef("float pi_approx(int n);")
ffibuilder.cdef("uint16_t crc16_update ( uint16_t crc, uint8_t data );")
ffibuilder.cdef("uint16_t get_crc16z(uint8_t *p, uint16_t len);")

ffibuilder.set_source("_crc",  # name of the output C extension
                        """
                            #include "crc.h" // the C header of the library
                        """,
                        sources=['crc.c'],  # includes pi.c as additional sources
                        libraries=['m'])  # on Unix, link with the math library






if __name__ == '__main__':
    #run this once
    ffibuilder.compile(verbose=True)


    #use this live
    from _crc.lib import pi_approx, get_crc16z

    print(pi_approx(1000000))
    data = ffibuilder.new("char[]", b"\x05\x01\x03\x7D\x02\x0E\x7E")
    result = get_crc16z(data, 7)
    print(result)
    data2 = ffibuilder.new("char[]", b"\x01\x00\x01\x00\x1a\x00\x00\x00\x00\x00\x00\x00\x00\x00\xfa\x00\x00\x00\x00\x00\x04\xa6\x58\x00\x00\x00\x00\x00\x00\x00\x08\xb5\x00\x00\x00\x00\x00\x00\x00\x00")
    data3 = ffibuilder.new("char[]", b"\x01\x00\x01\x00\x1a\x00\x00\x00\x00\x00\x00\x00\x00\x00\xfa\x00\x00\x00\x00\x00\x04\xa5\x58\x00\x12\x00\x00\x00\x00\x00\x00\xe3\x09\x00\x00\x00\x00\x00\x00\x00")

    result2 = get_crc16z(data2, 31)
    result3 = get_crc16z(data3, 31)
    print("First CRC16 ", result2)
    print("Last CRC16 ", result3)



