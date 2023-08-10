import ast
import binascii
import pandas as pd
import struct

#tamanhos: prefix 260, n sei 138

def hex_byte(string: str):
    e = ''.encode().hex() + string
    return bytearray.fromhex(e)

try:
    with open('C:\\Users\\Lucas\\Documents\\VS Projects\\Redstone\\translators\\textData.dat','rb') as f, open('C:\\Users\\Lucas\\Documents\\VS Projects\\Redstone\\translators\\textData_3.dat','wb') as nf:
        df = pd.read_excel('C:\\Users\\Lucas\\Documents\\VS Projects\\Redstone\\translators\\texttranslated.xlsx')
        f.read(117179)
        x = df['entxt'].values.tolist()
        bps = [b'\xe1\x08\x00\x00', b'\x06\x00\x00\x00', b'\x08\x00\x00\x00', b'\x11\x00\x00\x00', b'\x07\x00\x00\x00', b'\x14\x00\x00\x00', b'B\x00\x00\x00', b'%\x00\x00\x00', b'6\x00\x00\x00', b'U\x01\x00\x00', b'\x0c\x00\x00\x00', b'\n\x00\x00\x00', b'\x05\x00\x00\x00', b'\x04\x00\x00\x00', b'\r\x00\x00\x00', b'\x93\x00\x00\x00', b'(\x00\x00\x00']
        idxs = [0, 2273, 2279, 2287, 2304, 2311, 2331, 2397, 2434, 2488, 2829, 2841, 2851, 2856, 2860, 2879, 3026]
        i = 0
        for txt in x:
            if(i in [0, 2273, 2279, 2287, 2304, 2311, 2331, 2397, 2434, 2488, 2829, 2841, 2851, 2856, 2860, 2879, 3026]):
                nf.write(bps[0])
                bps.pop(0)
            i+=1
            if(txt.startswith('|')):
                print(txt)
                data = struct.pack('<h',int(len(txt[1:])/2))
                nf.write(data)
                data = hex_byte(txt[1:])
                nf.write(data)
                continue
            hex_txt = txt.encode('utf-8').hex() + '00'
            enlen = struct.pack('<h',int(len(hex_txt)/2))
            entxt_bhex = bytearray.fromhex(hex_txt)
            nf.write(enlen)
            nf.write(entxt_bhex)
        nf.write(f.read())
        f.close()
        nf.close()
except IOError:
  print('erro ao abrir arquivo')