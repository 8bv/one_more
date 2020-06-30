# -*- coding: utf-8 -*-

from dadata import Dadata
import pandas as pd
import numpy as np
from tqdm import tqdm

def parse(file):
    base = pd.read_excel(file)
    base = base.set_axis(
    ['card', 'organization', 'date',
    'from', 'town', 'store',
    'name', 'mail', 'date2'],
    axis=1
    )
    base['same'], base['okved'] = np.nan, np.nan

    pd.options.mode.chained_assignment = None
    # default='warn' for ignoring
    # 'A value is trying to be set on a copy of a slice from a DataFrame'
    for i in tqdm(range(len(base))):
        if base['organization'][i] is not np.nan:
            result = dadata.suggest("party", base['organization'][i])
            if len(result) == 0:
                base['same'][i] = "не найдено"
                base['okved'][i] = "пусто"
            elif len(result) == 1:
                base['same'][i] = "одна компания"
                base['okved'][i] = result[0]['data']['okved']
            else:
                base['same'][i] = "много подобных компаний"
                base['okved'][i] = result[0]['data']['okved']

    base = pd.merge(
    base, okved,
    how='left', left_on='okved', right_on='Новый код ОКВЭД'
    )
    base.drop(['Новый код ОКВЭД'], inplace=True, axis=1)
    base.to_excel(f'new_{file}', index=False)

def main():
    for file in os.listdir():
        parse(file)

if __name__ == '__main__':
    from token_holder import *
    import os
    dadata = Dadata(token)
    okved = pd.read_excel('new_okved.xlsx')
    directory = input('Папка с файлами: ')
    os.chdir(directory)
    main()
