from deep_translator import GoogleTranslator
import struct

def write_to_file(idxs,txts):
  new_list = []
  temp = ''
  for txt in txts:
    print(txt)
    temp+=txt + '|'
  temp = temp[:-1]
  temp = GoogleTranslator(source='auto',target='en').translate(temp)
  new_list = temp.split('|')
  print(len(new_list),len(txts))
  if(len(new_list) != len(txts)):
    new_list = []
    for txt in txts:
      temp = GoogleTranslator(source='auto',target='en').translate(txt)
      if(len(temp) > 254):
        raise Exception('Max length allowed is 254')
      new_list.append(temp)
  for id,txt in zip(idxs,new_list):
    nf.write(id)
    hex_txt = txt.encode().hex()
    hex_txt += ('0' * (256 - (len(hex_txt))))
    nf.write(bytearray.fromhex(hex_txt))

try:
  with open('C:\\Users\\Lucas\\Documents\\VS Projects\\Redstone\\translators\\textData.dat','rb') as f, open('C:\\Users\\Lucas\\Documents\\VS Projects\\Redstone\\translators\\textData_2.dat','wb') as nf:
      nf.write(f.read(119076))
      txts = []
      idxs = []
      read_so_far = 0
      id = f.read(1)
      while id.hex() != '64010000':
        id = f.read(4)
        if(id.hex() == '22010000'):
          write_to_file(idxs,txts)
          txts = []
          idxs = []
          read_so_far = 0
          nf.write(f.read(256))
          continue
        idxs.append(id)
        temp_hex = f.read(1)
        hex = temp_hex.hex()
        while temp_hex != '00':
          temp_hex = f.read(1).hex()
          hex += temp_hex
        txt = bytes.fromhex(hex).decode('Shift-JIS')[:-1]
        txts.append(txt)
        read_so_far += len(txt)
        restante = 256-int(len(hex)/2)
        f.read(restante)
        if(read_so_far > 2400):
          write_to_file(idxs,txts)       
          txts = []
          idxs = []
          read_so_far = 0
      nf.write(f.read())
      f.close()
      nf.close()
except IOError:
  print('erro ao abrir arquivo')