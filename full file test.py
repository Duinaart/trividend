##################################
# Table scraping imports
import os
import glob
import tabula
import pandas as pd
pd.options.display.width = 0
pd.set_option('display.max_rows', None)
pd.options.mode.chained_assignment = None  # default='warn'

###################################
#? Get client names and firm_numbers
xls = pd.read_excel('Opvolgingsdocument Leads.xlsx', 'Klanten')
firm_names = xls['Klant'].to_list()
firm_numbers = xls['Number'].to_list()
print(firm_numbers, firm_names)

########################################################################################
#! Extract tables from pdf and convert to one firm data
#! Make data in such a way that every column has new year with same index of GAAP
########################################################################################
#######################################
#? Activa
######################################
def main():
    for i in range(0, len(firm_numbers)):

        files = sorted(glob.glob('/home/emile/Documents/02 - KUL/3e bachelor/Bachelorproef/jaarrekeningen/'
                                 '{}/*.pdf'.format('Oud Wijzer vzw')))
        final_dfs = []

        for file in files:
            basename = os.path.basename(file)
            current_year = int(basename.split('-')[0]) - 1
            previous_year = int(current_year) - 1

            data = load_data(file)

            final = pd.concat(clean_every_pdf(data, current_year))
            final.reset_index(inplace=True, drop=True)
            final.drop(previous_year, axis=1, inplace=True, errors='ignore')

            final_dfs.append(final)
        final_firm = pd.concat(final_dfs, axis=1, join="inner")
        final_firm = final_firm.loc[:, ~final_firm.columns.duplicated()]
        final_firm.to_csv('/home/emile/Documents/02 - KUL/3e bachelor/Bachelorproef/jaarrekeningen/'
                                 '{}/', '{}.csv'.format(firm_names[i], firm_names[i]))

#############################################################################
#? functions
#############################################################################
# Read data from pdf with tabula and make it a df
def load_data(file):
    df_list = []
    for i in range(1,8):
        df1 = tabula.read_pdf(file, output_format='dataframe', pages=i, multiple_tables=True)
        df = df1[0] if len(df1) else pd.DataFrame()
        df_list.append(df)
    df_list2 = [j for j in df_list if j.size >= 25]
    return df_list2

def clean_every_pdf(data, current_year):
    cleaned_dfs = []
    for df in data:
        df.columns = df.iloc[0]
        df = df[1:]
        df = df.dropna(how='all', axis=1)
        df.reset_index(inplace=True)
        df.columns.name = None
        df.drop('Vorig boekjaar', axis=1, inplace=True, errors='ignore')
        df.rename(columns={'Boekjaar': current_year}, inplace=True)
        df.drop('level_1', axis=1, inplace=True)
        df.rename(columns={'level_0': "Beschrijving"}, inplace=True)

        # test to see if it works for every part of the thing
        df.drop('level_2', axis=1, inplace=True, errors='ignore')
        df.rename(columns={'level_3': 'Codes'}, inplace=True, errors='ignore')

        cleaned_dfs.append(df)

    return cleaned_dfs



#############################
#  run
#############################
if __name__ == '__main__':
    main()
