import struct
import pandas as pd

#tamanhos: prefix 260, n sei 138

def hex_byte(string: str):
    e = ''.encode().hex() + string
    return bytearray.fromhex(e)

def generate_trans_text(path, delete_etiquette: bool = False):
    """
    Generates new textData based on sheet texttranslated.xlsx
    @params:
    path - folder that contains both textdat.dat and texttranslated.xlsx
    """
    try:
        with open(path+'\\textData.dat','rb') as f, open(path+'\\textData_3.dat','wb') as nf:

            while(f):

            # #-----------------------------------------------------------------------------------------------------------------------
            # df = pd.read_excel(path+'\\texttranslated.xlsx')
            # x = df['entxt'].values.tolist()
            # total_read = 0
            # for txt in x:
            #     if(total_read in [0,99293,99401,99463,99620,99733,99961,103864,104533,107413,110585,111579,111742,111797,111855,11961,112876,115262]):
            #     # idx [0, 2273, 2279, 2287, 2304, 2311, 2331, 2397, 2434, 2488, 2829, 2841, 2851, 2856, 2860, 2879, 3026]
            #         data = f.read(4)
            #         print('breakpoint(hex):', data.hex())
            #         nf.write(data)
            #         total_read += 4
            #     data_l = f.read(2)
            #     dlen = int.from_bytes(data_l, byteorder='little')
            #     data_t = f.read(dlen)
            #     total_read += dlen+2
            #     if(txt.startswith('|')):
            #         nf.write(data_l)
            #         nf.write(data_t)
            #         continue
            #     hex_txt = txt.encode('utf-8').hex() + '00'
            #     enlen = struct.pack('<h',int(len(hex_txt)/2))
            #     entxt_bhex = bytearray.fromhex(hex_txt)
            #     nf.write(enlen)
            #     nf.write(entxt_bhex)          
            # print(total_read)
            # #-----------------------------------------------------------------------------------------------------------------------
            # #nao sei
            # nf.write(f.read(1898))
            # #prefixes
            # f.read(145860)
            # #-----------------------------------------------------------------------------------------------------------------------
            # df = pd.read_excel('C:\\Users\\Lucas\\Documents\\VS Projects\\Redstone\\translators\\prefix.xlsx')
            # ids = df['idx'].values.tolist()
            # txts = df['new_txt'].values.tolist()
            # for id,txt in zip(ids,txts):
            #     b_id = hex_byte(id)
            #     if(txt == 'Breakpoint'):
            #         nf.write(b_id)
            #         continue
            #     hex_txt = txt.encode('utf-8').hex()
            #     remaning = 256-int(len(hex_txt)/2)
            #     hex_txt += '00' * remaning
            #     entxt_bhex = bytearray.fromhex(hex_txt)
            #     nf.write(b_id)
            #     nf.write(entxt_bhex)
            # nf.write(f.read())
            # f.close()
            # nf.close()
    except IOError:
        print('erro ao abrir arquivo')
    except KeyError as err:
        print('coluna '+err.keys()+'não encontrada')

def export_jp_text(path:str):
    """
    Extract japanese text from textdata.dat and export to a .xlsx sheet
    @params:
    path - folder that contains textData.dat file
    """
    try:
        #with open(path+'\\textData.dat','rb') as f:
        with open('/content/drive/MyDrive/red texttrans/textData.dat','rb') as f:
            df = pd.DataFrame(columns=['jlen','jtxt'])
            for _ in range(18):
                idx_count = int.from_bytes(f.read(4),byteorder='little')
                new_row = {'jlen': idx_count,'jtxt': 'idx count'}
                df.loc[len(df)] = new_row
                while idx_count > 0:
                    dlen = int.from_bytes(f.read(2), byteorder='little')
                    txt = f.read(dlen)
                    print(idx_count,str(txt[:-1],'Shift-JIS'),txt.hex())
                    new_row = {'jlen': dlen,'jtxt': str(txt[:-1],'Shift-JIS')}
                    df.loc[len(df)] = new_row
                    idx_count -= 1
            f.close()
            #df.to_excel(path+'\\texttranslated.xlsx')
            #df.to_excel('/content/drive/MyDrive/red texttrans/teste_refactor.xlsx')
    except IOError:
        print('erro ao abrir arquivo')

export_jp_text('')

