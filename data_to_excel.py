import pandas as pd
import os

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
    if(data_chunk % (data_length+index_size) != 0 or num_indexes % (data_length+index_size) != 0):
        raise Exception('Check @data_chunk or @num_indexes. Number of items is not precise')
    if(data_chunk):
        read = data_chunk
    elif(num_indexes):
        read = num_indexes

    with open(file,'rb') as f:
        try:
            if ignore: f.read(ignore)
            df = pd.DataFrame(columns=['idx','txt','max_len','enlen' ,'entxt'])
            while read != 0:
                idx = f.read(index_size).hex()
                data = f.read(data_length)
                aux = data[:1]
                temp = aux
                step = 1
                while(aux != b'\x00'):
                    aux = data[step:step+1]
                    temp += aux
                    step+=1
                txt = temp[:-1].decode(charset)
                #print(idx,txt)
                new_row = {'idx': idx,'txt': txt,'max_len': data_length, 'enlen' : '' ,'entxt' :'=GOOGLETRANSLATE(\"%s\";\"auto\";\"en\")' % txt}
                df.loc[len(df)] = new_row
                print(read)
                if(data_chunk):
                    read -= data_length+index_size
                elif(num_indexes):
                    read -= 1
                print(read)
            f.close()
            path = os.path.dirname(os.path.abspath(__file__)) + '\\'
            df.to_excel(path+output+'.xlsx')
        except IOError as e:
            print(e.strerror)

#prefix filters
#read_file('C:\\Users\\Lucas\\Documents\\VS Projects\\Redstone\\translators\\Mangchi_en.exe',num_indexes=176,ignore=4100944,output='filters',charset='cp949',data_length=128)
#read_file('C:\\Users\\Lucas\\Documents\\VS Projects\\Redstone\\translators\\Mangchi_en.exe',data_chunk=4012,ignore=2915564,output='teste',charset='cp949',data_length=64,has_subdata=[32,32])
read_file('C:\\Users\\Lucas\\Documents\\VS Projects\\Redstone\\translators\\Mangchi_en.exe',data_chunk=5780,ignore=2922364,output='teste',charset='cp949',data_length=64,index_size=4)#num_indexes=85
    