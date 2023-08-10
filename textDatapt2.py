from deep_translator import GoogleTranslator
import struct

try:
  with open('C:\\Users\\Lucas\\Documents\\VS Projects\\Redstone\\translators\\textData.dat','rb') as f:#, open('C:\\Users\\Lucas\\Documents\\VS Projects\\Redstone\\translators\\textData_2.dat','wb') as nf:
        #nf.write(f.read(117179))
        data = f.read(117179)
        data = f.read(1898)
        #145268
        #AF000000 BP #211897
        #1D000000 BP #257401
        #0f000000 BP? #264945
        #data = f.read(92820)
        data = f.read(4)
        data = f.read(15)
        print(str(data,'shift-jis'))
        # data = f.read(45500)
        # data = f.read(4)
        # data = f.read(7540)
        print(data.hex())
        f.close()
        #nf.close()
except IOError as e:
   print(e.strerror)
   