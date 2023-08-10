import re
import pandas

sheet = 'C:\\Users\\Lucas\\Documents\\VS Projects\\Redstone\\translators\\teste.xlsx'

df = pandas.read_excel(sheet)

df.loc[:,'newtxt'] = df.loc[:, 'newtxt'].str.lower()

df.to_excel(sheet)

  