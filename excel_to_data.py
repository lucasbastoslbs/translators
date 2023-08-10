import pandas as pd

#tamanhos: prefix 260, n sei 138
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
            ids = df['idx'].values.tolist()
            txts = df['entxt'].values.tolist()
            for id,txt in zip(ids,txts):
                b_id = hex_byte(id)
                f.read(int(len(id)/2))
                # if(txt == 'Breakpoint'):
                #     nf.write(b_id)
                #     continue
                hex_txt = txt.encode('utf-8').hex()
                remaning = data_length-int(len(hex_txt)/2)
                hex_txt += '00' * remaning
                entxt_bhex = bytearray.fromhex(hex_txt)
                f.read(data_length)
                nf.write(b_id)
                nf.write(entxt_bhex)
                for i in has_subdata[1:]:
                    nf.write(f.read(i))                
            nf.write(f.read())
            f.close()
            nf.close()
    except IOError as e:
        print(e.strerror)

#files
exe = 'C:\\Users\\Lucas\\Documents\\VS Projects\\Redstone\\translators\\Mangchi_en.exe'
sheet = 'C:\\Users\\Lucas\\Documents\\VS Projects\\Redstone\\translators\\teste.xlsx'
#write_file(exe,sheet,data_length=128,ignore=4100944)
#write_file(exe,sheet,data_length=128,ignore=2553608)
#write_file(exe,sheet,data_length=32,ignore=2915564,has_subdata=[32,32])
write_file(exe,sheet,data_length=32,ignore=2922364,has_subdata=[32,32])