import pandas as pd

from functions import ratio_df


unique_years = ratio_df['Jaar'].unique().tolist()

average_list = []
for year in unique_years:
    yearly_df = ratio_df[ratio_df['Jaar'] == year]
    average_list.append(yearly_df.mean())

average_df = pd.DataFrame(average_list).round(2)
average_df.Jaar = pd.to_datetime(average_df.Jaar, format='%Y').dt.year
average_df.set_index('Jaar', inplace=True, drop=True)

print(average_df)



