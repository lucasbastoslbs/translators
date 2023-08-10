#this is only for event list -- so far

import pandas as pd
import os
import re

def translatecolumn_to_text(sheet):
    df = pd.read_excel(sheet)
    newm = []
    newd = []
    for m,d in zip(df['enmtxt'].values.tolist(),df['endtxt'].values.tolist()):
        temp = m.lower()
        temp = temp.replace('] ', ']')
        temp = temp.replace(' [', '[')
        newm.append(temp)
        temp = d.lower()
        temp = temp.replace('] ', ']')
        temp = temp.replace(' [', '[')
        newd.append(temp)
        print(temp)
    #df['newmtxt'] = newm
    #df['newdtxt'] = newd
    #df.to_excel(sheet)

def get_readable_text(data:bytearray, charset: str = 'utf-8'):
    aux = data[:1]
    temp = aux
    step = 1
    while(aux != b'\x00'):
        aux = data[step:step+1]
        temp += aux
        step+=1
    try:
        txt = temp[:-1].decode(charset)
    except Exception as e:
        print(e.args)
    return txt

def hex_byte(string: str):
    e = ''.encode().hex() + string
    return bytearray.fromhex(e)

def write_file(file,sheet, data_length: int = 0, ignore: int | None = 0, has_subdata: list[int] = []):
    """
    Writes a file based on provided data sheet. For fixed data length.

    params:
    @file: data file path
    @sheet: sheet file path
    @data_length: bytes each cell must have
    @ignore: bytes to be ignored before writing
    """
    # if has_subdata and data_length:
    #     if data_length/sum(has_subdata) != 1:
    #         raise Exception('@data_length and @has_subdata must have same absolute value')

    try:
        with open(file,'rb') as f, open(file+'.new','wb') as nf:
            if(ignore):
                nf.write(f.read(ignore))
            df = pd.read_excel(sheet)
            mtxts = df['newmtxt'].values.tolist()
            dtxts = df['newdtxt'].values.tolist()
            for txt1,txt2 in zip(mtxts,dtxts):
                f.read(64)
                hex_txt = txt1.encode('utf-8').hex()
                remaning = 64-int(len(hex_txt)/2)
                hex_txt += '00' * remaning
                entxt_bhex = bytearray.fromhex(hex_txt)
                nf.write(entxt_bhex)
                nf.write(f.read(2))
                f.read(256)
                hex_txt = txt2.encode('utf-8').hex()
                remaning = 256-int(len(hex_txt)/2)
                hex_txt += '00' * remaning
                entxt_bhex = bytearray.fromhex(hex_txt)
                nf.write(entxt_bhex)
            nf.write(f.read())
            f.close()
            nf.close()
    except IOError as e:
        print(e.strerror)

def read_file(file : str, charset: str | None = 'utf-8', data_chunk: int | None = 0, data_length: int = 0, ignore: int | None = 0, index_size: int = 4, num_indexes: int | None = 0, output: str | None = 'new'):
    """
    read_file reads a file that it's structs is like [IDX][DATA](specific length).
    params:
    @file: string file path
    @data_chunk: number of bytes from the chunk to get extracted text
    @data_length: data length for the text to be read;
    @ignore: number of bytes to be ignored before command;
    @num_indexes: can be used instead of passing data size. This param will define how many loops will be read;
    @charset: encoding for the text to be translated. 'cp949' for kr, 'shift-jis' for jp
    @output: name of excel output file 'defult = new.xlsx'
    """
    if(not data_chunk and not num_indexes):
        raise Exception('At least one of @data_chunk or @num_indexes parameters must be given.')
    if not data_length:
        raise Exception('Data length (int) must be given')
    if(data_chunk):
        read = data_chunk
    elif(num_indexes):
        read = num_indexes

    with open(file,'rb') as f:
        try:
            if ignore: f.read(ignore)            
            df = pd.DataFrame(columns=['mlen','mtxt','dlen','dtxt','enmtxt','endtxt'])
            while read != 0:
                data = f.read(data_length)
                txt = get_readable_text(data[:64],charset)
                txt2 = get_readable_text(data[66:],charset)                    
                #new_row = {'idx': idx,'txt': txt,'max_len': data_length, 'enlen' : '' ,'entxt' :'=GOOGLETRANSLATE(\"%s\";\"auto\";\"en\")' % txt}
                new_row = {'mlen':64,'mtxt':txt,'dlen':256,'dtxt':txt2,'enmtxt':'' ,'endtxt':''}
                print(txt,'#',txt2)
                df.loc[len(df)] = new_row
                if(data_chunk):
                    read -= data_length
                elif(num_indexes):
                    read -= 1
            f.close()
            path = os.path.dirname(os.path.abspath(__file__)) + '\\'
            df.to_excel(path+output+'.xlsx')
        except IOError as e:
            print(e.strerror)

exe = 'C:\\Users\\Lucas\\Documents\\VS Projects\\Redstone\\translators\\Mangchi_en.exe'
sheet = 'C:\\Users\\Lucas\\Documents\\VS Projects\\Redstone\\translators\\conditionals.xlsx'
#prefix filters
#read_file('C:\\Users\\Lucas\\Documents\\VS Projects\\Redstone\\translators\\Mangchi_en.exe',num_indexes=176,ignore=4100944,output='filters',charset='cp949',data_length=128)
#read_file('C:\\Users\\Lucas\\Documents\\VS Projects\\Redstone\\translators\\Mangchi_en.exe',data_chunk=4012,ignore=2915564,output='teste',charset='cp949',data_length=64,has_subdata=[32,32])
#read_file('C:\\Users\\Lucas\\Documents\\VS Projects\\Redstone\\translators\\Mangchi_en.exe',data_chunk=5780,ignore=2922364,output='teste',charset='cp949',data_length=64,index_size=4)#num_indexes=85

#event list - reactions
#read_file('C:\\Users\\Lucas\\Documents\\VS Projects\\Redstone\\translators\\Mangchi_en.exe',data_chunk=54418,ignore=2947952,output='teste',charset='cp949',data_length=322)
#write_file(exe,sheet,data_length=322,ignore=2947952)

#event list - conditions
#read_file(exe,'cp949',data_length=322,ignore=3394730,output='conditionals',data_chunk=49910)
#translatecolumn_to_text(sheet)
#write_file(exe,sheet,data_length=322,ignore=3394730)
