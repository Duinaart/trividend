import numpy as np
import pandas as pd
pd.options.display.width = 0
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.options.mode.chained_assignment = None  # default='warn'

df = pd.read_excel('gedetailleerde_data.xlsx', index_col=0)
df.fillna(0, inplace=True)
df.reset_index(inplace=True, drop=True)

#! Kortetermijnliquiditeit
df["Ratio's"] = np.NAN
df['Aangepaste vlottende activa'] = df[['Voorraden', 'Handelsvorderingen op ten hoogste 1 jaar',
                                        'Overige vorderingen op ten hoogste 1 jaar',
                                        'Geldbeleggingen',
                                        'Liquide middelen']].sum(axis=1) #vorderingen > 1 jaar erbij
df['Current Ratio'] = df['Aangepaste vlottende activa'] / \
                      (df[['Schulden op ten hoogste één jaar', 'Overlopende rekeningen']].sum(axis=1))
df['Quick Ratio'] = (df['Aangepaste vlottende activa'] - df['Voorraden'])\
                    / df['Schulden op ten hoogste één jaar']


#! Bedrijfsprestaties
df['Bedrijfsactiva'] = df[['Oprichtingskosten', 'Immateriële vaste activa', 'Materiële vaste activa', 'Voorraden',
                           'Handelsvorderingen op ten hoogste 1 jaar']].sum(axis=1)
df['Rendabiliteit bedrijfsactiva'] = df['Courant resultaat vóór belasting (+/-)'] / df['Bedrijfsactiva']
df['Brutorendabiliteit totale activa'] = (df[['Winst (Verlies) van het boekjaar na belasting (+/-)',
                                             'Afschrijvingen en waardeverminderingen op oprichtingskosten, immateriële '
                                             'en materiële vaste activa', 'Waardeverminderingen op voorraden,'
                                                                          ' bestellingen in uitvoering, handelsvorderingen' ]].sum(axis=1)
                                          - df['Onttrekking aan de uitgestelde belastingen']) / df['Totaal der activa']
df['Nettorendabiliteit totale activa'] = df[['Winst (Verlies) van het boekjaar na belasting (+/-)',
                                             'Belastingen op het resultaat (+/-)', 'Financiële kosten']].sum(axis=1) \
                                         / df['Totaal der activa']
df['Nettorendabiliteit eigen vermogen'] = df[['Winst (Verlies) van het boekjaar na belasting (+/-)',
                                              'Belastingen op het resultaat (+/-)']].sum(axis=1) \
                                          / df['Eigen vermogen'] # Resultaat boekjaar of Winst nemen?

# df['Bruto toegevoegde waardemarge'] = df['Toegevoegde waarde (Excl. BTW)'] / df['Courant resultaat vóór belasting (+/-)']
 # -> herbekijken (courant resultaat zitten kosten in verwerkt - moeten resultaat zijn) (overbodig)

#! Analyse financiële structuur
df['Financiële onafhankelijkheid'] = df['Eigen vermogen'] / df['Totaal der passiva'] #beste
# df['Algemene schuldgraad'] = (df['Totaal der passiva'] - df['Eigen vermogen'] ) / df['Totaal der passiva']

df['Financieringsstabiliteit'] = df[['Eigen vermogen', 'Schulden op meer dan één jaar']].sum(axis=1) \
                                 / df['Totaal der passiva']
df['Operationele kasstroom'] = df[['Winst (Verlies) van het boekjaar na belasting (+/-)',
                                   'Afschrijvingen en waardeverminderingen op oprichtingskosten, '
                                   'immateriële en materiële vaste activa']].sum(axis=1)
df['Aflossingscapaciteit'] = df['Operationele kasstroom'] \
                             / df[['Financiële schulden op meer dan 1 jaar', 'Financiële schulden op ten hoogste 1 jaar']].sum(axis=1)

df['NBK'] = df['Aangepaste vlottende activa'] - df['Schulden op ten hoogste één jaar']
df['Nettothesaurie'] = df[['Geldbeleggingen', 'Liquide middelen']].sum(axis=1) - df['Financiële schulden op ten hoogste 1 jaar']

df.set_index(['Bedrijf'], inplace=True)
ratio_df = df.iloc[:, 133:]
# ratio_df.reset_index(inplace=True, drop=True)

# print(df.loc['TWERK'])
# print(ratio_df.loc['TWERK'])


# ratio_df.to_excel('ratio_trividend.xlsx')
# df.to_excel('full_Trividend.xlsx')


