import pandas as pd
pd.options.display.width = 0
pd.set_option('display.max_rows', None)
pd.options.mode.chained_assignment = None  # default='warn'
import re

#! weet niet of validiteit van data goed is want mankeert essentiële informatie precies
balans = pd.read_excel('Balans.xlsx',
                       header=None,
                       sheet_name=None,
                       )
rr = pd.read_excel('RR.xlsx',
                   header=None,
                   sheet_name=None,
                   )

balans_list = list(balans.values())
rr_list = list(rr.values())


names = []
def clean_excel(df, names):
    name = df.loc[0][1]
    names.append(name)

    if len(df.index) > 90:
        column_names = df.loc[[12]].values.tolist()[0] # Balans
        dirty_column_names = [x for x in column_names if str(x) != 'nan'][1:]
        clean_years = []
        for i in dirty_column_names:
            clean_years.append(i.replace("\nEUR", ""))
    else:
        column_names = df.loc[[11]].values.tolist()[0] # RR
        dirty_column_names = [x for x in column_names if str(x) != 'nan'][1:]
        clean_years = dirty_column_names

    clean_years.insert(0, 'Jaar')


    if len(df.index) > 90:
        df = df.iloc[13:, :]        # start dataframa where data starts (balans)
    else:
        df = df.iloc[13: , :]        #start dataframa where data starts (RR)
    df = df.dropna(axis='columns', thresh=7)
    df = df.dropna(axis=0, how='all')
    df.columns = clean_years
    df = df.T

    return df, names


def getlistdf(df_list):
    full_df = []
    for i in df_list:
        output = clean_excel(i, names)
        df = output[0]
        df.reset_index(inplace=True)
        df.columns = df.iloc[0]
        df = df.iloc[1:]
        df = df.loc[:, ~df.columns.duplicated()]
        name = output[1][-1]            # firm name is always appended to previous list, so take last element
        df.insert(0, 'Bedrijf', name)
        full_df.append(df)

    return full_df

balans_dfs = getlistdf(balans_list)
rr_dfs = getlistdf(rr_list)

def concat_dfs(df_list):
    df = pd.concat(df_list)
    df.reset_index(drop=True, inplace=True)
    # balans_df.drop(['Algemeen formaat', 'Niet geconsolideerde rekeningen'], axis=1, inplace=True)
    # balans_df.set_index(['Bedrijf', 'Jaar'], inplace=True)
    df = df.rename(columns=lambda x: x.strip())
    df = df.loc[:, ~df.columns.duplicated()]
    numeric = df.columns.tolist()[2:]
    df[numeric] = df[numeric].apply(pd.to_numeric, errors='coerce')
    df = df.reset_index(drop=True)

    return df

balans_df = concat_dfs(balans_dfs)
balans_df.to_excel('gedetailleerde_balans.xlsx')
rr_df = concat_dfs(rr_dfs)
rr_df.to_excel('gedetailleerde_rr.xlsx')


# final_df = pd.concat([balans_df, rr_df], axis=1, join='inner')
# print(final_df)

# balans_df.to_csv('worksheet_trividend.csv')
# final_df.to_excel('gedetailleerde_data.xlsx')

