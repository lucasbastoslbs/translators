import pandas as pd
import os

def read_file_random_length(file : str, charset: str | None = 'utf-8', data_chunk: int | None = 0, starting_byte: int | None = 0, output: str | None = 'new'):
    """
    read_file reads a file that it's structs is like [IDX][DATA](random length) but continous.
    params:
    @file: string file path
    @data_chunk: number of bytes from the chunk to get extracted text
    @starting_byte: number of bytes to be ignored before command;
    @charset: encoding for the text to be translated. 'cp949' for kr, 'shift-jis' for jp
    @output: name of excel output file 'defult = new.xlsx'
    """
    if(not data_chunk):
        raise Exception('@data_chunk parameter must be given.')
    with open(file,'rb') as f:
        try:
            if starting_byte: f.read(starting_byte)
            df = pd.DataFrame(columns=['max_len','txt','enlen','entxt'])
            data = f.read(data_chunk)
            step = 0
            allowed_size = 0
            while step < data_chunk:
                aux = data[step:step+1]
                temp = aux
                allowed_size = step
                step+=1                
                while(aux != b'\x00'):
                    aux = data[step:step+1]
                    temp += aux
                    step+=1
                step-=1
                txt = temp[:-1].decode(charset)
                print(txt)
                aux = data[step:step+1]
                while(aux == b'\x00'):
                    aux = data[step:step+1]
                    step+=1
                step-=1
                allowed_size = step - allowed_size - 1
                new_row = {'max_len': allowed_size,'txt': txt,'enlen':'','entxt':'=GOOGLETRANSLATE(\"%s\";\"auto\";\"en\")' % txt}
                df.loc[len(df)] = new_row
            f.close()
            path = os.path.dirname(os.path.abspath(__file__)) + '\\'
            df.to_excel(path+output+'.xlsx')
        except IOError as e:
            print(e.strerror)

def hex_byte(string: str):
    e = ''.encode().hex() + string
    return bytearray.fromhex(e)

def write_file_random_length(file,sheet, starting_byte: int | None = 0, original_data_chunk: int = 0):
    """
    Writes a file based on provided data sheet. For random length.
    ***IMPORTANT***: data must be continuous

    params:
    @file: data file path
    @sheet: sheet file path
    @starting_byte: bytes to be ignored before writing
    """
    try:
        with open(file,'rb') as f, open(file+'.new','wb') as nf:
            if(starting_byte):
                nf.write(f.read(starting_byte))
            df = pd.read_excel(sheet)
            ids = df['max_len'].values.tolist()
            txts = df['entxt'].values.tolist()
            for id,txt in zip(ids,txts):
                data_length = int(id)
                hex_txt = txt.encode('utf-8').hex()
                remaning = data_length-int(len(hex_txt)/2)
                hex_txt += '00' * (remaning+1)
                entxt_bhex = bytearray.fromhex(hex_txt)
                nf.write(entxt_bhex)
            f.read(original_data_chunk)
            nf.write(f.read())
            f.close()
            nf.close()
    except IOError as e:
        print(e.strerror)

#files
exe = 'C:\\Users\\Lucas\\Documents\\VS Projects\\Redstone\\translators\\Mangchi_en.exe'
sheet = 'C:\\Users\\Lucas\\Documents\\VS Projects\\Redstone\\translators\\teste.xlsx'

#write_file(exe,sheet,data_length=128,starting_byte=4100944)


#prefix filters
#read_file('C:\\Users\\Lucas\\Documents\\VS Projects\\Redstone\\translators\\Mangchi_en.exe',num_indexes=176,starting_byte=4100944,output='filters',charset='cp949',data_length=128)
#mangchi 2553608-2562568 - KARMA_DETAIL_WINDOW
#read_file_random_length(exe,data_chunk=14124,starting_byte=2553608,output='teste',charset='cp949')
#write_file_random_length(exe,sheet,starting_byte=2553608,original_data_chunk=14124)
#mangchi 2550300-2550467
#read_file_random_length(exe,data_chunk=168,starting_byte=2550300,output='teste',charset='cp949')
write_file_random_length(exe,sheet,starting_byte=2550300,original_data_chunk=168)