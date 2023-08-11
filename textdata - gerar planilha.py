import struct
import pandas as pd

#tamanhos: prefix 260, n sei 138
df = pd.DataFrame(columns=['jlen','jtxt'])

def translate_pack(lista):
  string=''
  a = len(lista)
  for i in lista:
    string += i.strip() + '|'
  string = string[:-1]
  #print(string)
  try:
    string = GoogleTranslator(source='auto', target='en').translate(string)
  except:
    print('problema api tradutor')
  #print(string)
  new_lista = string.split('|')
  if(len(lista) != len(new_lista)):
    new_lista = slow_translate_pack(lista)
  print(len(lista),',',len(new_lista))
  for j,e in zip(lista,new_lista):
    new_row = {'jlen': len(j),'jtxt': j,'enlen': len(e),'entxt': e}
    df.loc[len(df)] = new_row
  return new_lista

def slow_translate_pack(lista):
  new_lista = []
  for i in lista:
    try:
      txt = GoogleTranslator(source='auto', target='en').translate(i)
      new_lista.append(txt)
      print(i,txt)
    except:
      print('problema api tradutor slow')
  return new_lista


def save_file(txts):
  try:
    txts = translate_pack(txts)
  except:
    print('fail translate')
  for txt in txts:
    try:
      if(txt == ''):
        enlen = struct.pack('<h',2)
        entxt_bhex = bytearray.fromhex('2000')
      else:
        if(txt == None):
          enlen = struct.pack('<h',3)
          hex_txt = '819300'.encode('utf-8').hex()
          txt = '819300'
        else:
          enlen = struct.pack('<h',len(txt)+1)
          hex_txt = txt.encode('utf-8').hex() + '00'
        entxt_bhex = bytearray.fromhex(hex_txt)
      nf.write(enlen)
      nf.write(entxt_bhex)
    except IOError:
      print('problema no arquivo')
def extract_jp_text(path:str):
  abspath = path.split(path.)
  try:
    with open('/content/drive/MyDrive/red texttrans/textData.dat','rb') as f, open('/content/drive/MyDrive/red texttrans/textData_3.dat','wb') as nf:
        data = f.read(4)
        total_read = 4
        txts = []
        read_so_far = 0
        nf.write(data)
        while total_read < 117179:
        #for _ in range(150):
          if(read_so_far > 2000):
            print(total_read)
            save_file(txts)
            read_so_far = 0
            txts = []
          data = f.read(2)
          dlen = int.from_bytes(data, byteorder='little')
          read_so_far += dlen
          txt = f.read(dlen)
          txts.append(str(txt[:-1],'Shift-JIS'))
          total_read += dlen+2
          if(total_read in [99293,99401,99463,99620,99733,99961,103864,104533,107413,110585,111579,111742,111797,111855,112876,115262]):
          # idx [2272, 2278, 2286, 2303, 2310, 2330, 2396, 2433, 2487, 2828, 2840, 2850, 2855, 2859, 2877, 3024]
            save_file(txts)
            print(total_read)
            read_so_far = 0
            txts = []
            nf.write(f.read(4))
            total_read += 4
          elif total_read in [111961]:
          # idx [2872]
            print(total_read)
            save_file(txts)
            read_so_far = 0
            txts = []
            nf.write(f.read(8))
            total_read += 8
        if(len(txts) > 0):
          save_file(txts)
        nf.write(f.read())
        f.close()
        nf.close()
        df.to_excel('/content/drive/MyDrive/red texttrans/texttranslated.xlsx')
  except IOError:
    print('erro ao abrir arquivo')