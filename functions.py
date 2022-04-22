import pandas as pd
import plotly.graph_objects as go

pd.options.display.width = 0
pd.set_option('display.max_rows', None)
pd.options.mode.chained_assignment = None  # default='warn'

######################################################################################################################
# ! Formatting of dataframes
######################################################################################################################
# ! format dataframe to make more sense
normal_df = pd.read_excel('gedetailleerde_data.xlsx', usecols='B:EF', index_col=0)
ratio_df = pd.read_excel('ratio_trividend.xlsx', index_col=0)
participaties = pd.read_excel('participaties.xlsx', index_col=None)[:-1].iloc[:, :-2]
leningen = pd.read_excel('leningen.xlsx', index_col=None)[:-1].iloc[:, :-2]

normal_df.Jaar = pd.to_datetime(normal_df.Jaar, infer_datetime_format=True).dt.year
ratio_df.Jaar = pd.to_datetime(ratio_df.Jaar, infer_datetime_format=True).dt.year
participaties.Jaar = pd.to_datetime(participaties.Jaar, format='%Y').dt.year
leningen.Jaar = pd.to_datetime(leningen.Jaar, format='%Y').dt.year

######################################################################################################################
# ! Input Field
######################################################################################################################
firm = 'CHASE CREATIVE'
unique_firms = sorted(normal_df.index.unique().tolist())[1:]


######################################################################################################################
# ! Functions
######################################################################################################################
def investeringsoutputs(firm):
    bedrijf = firm.upper()
    participatie_check = participaties.loc[participaties['Participaties'] == '{}'.format(bedrijf)]
    if len(participatie_check.index) > 0:
        participatie = participatie_check.iloc[0]
        aankoopbedrag = participatie['Aankoopprijs']
        participatie_jaar = participatie['Jaar']

    else:
        aankoopbedrag = 0
        participatie_jaar = 2100 # -> check how we can return NaN value ofzo, anders probleem met lijst

    bedrijf_ouput = 'Het geselecteerde bedrijf is {}'.format(bedrijf)

    if aankoopbedrag == 0:
        participatie_output = 'Trividend nam geen participatie op in het bedrijf.'
    else:
        participatie_output = 'Trividend nam een participipatie op van {} in {}'.format(
            "€{:,.2f}".format(aankoopbedrag), participatie_jaar)

    print(leningen)
    lening = leningen.loc[leningen['Leningen'] == '{}'.format(bedrijf)]
    leningbedrag = lening['Leningbedrag'].sum()
    total_investment = aankoopbedrag + leningbedrag

    df = ratio_df.loc['{}'.format(bedrijf)]

    if len(lening.index) > 0:
        eerste_lening = lening.iloc[0]
        lening_jaar = eerste_lening['Jaar']
        lening_tekst = 'Trividend leende de volgende bedragen:'
        lening_output = lening

        earliest_investment = min(participatie_jaar, lening_jaar)

    else:
        earliest_investment = participatie_jaar
        lening_tekst = 'Trividend heeft geen lening aangeboden'
        lening_output = pd.DataFrame()

    if len(lening_output.index) > 0:
        investeringen = (lening_output['Jaar'].tolist())
    else:
        investeringen = []
    if participatie_jaar != 2100:
        investeringen.append(participatie_jaar)
    investeringen = list(set(investeringen))
    investeringen_aangepast = [x - 1 for x in investeringen]

    investeringsjaar = 'De eerste investering werd gemaakt in {}.'.format(earliest_investment)
    geinvesteerd_bedrag = 'Het totale geinvesteerde bedrag bedraagt {}.'.format("€{:,.2f}".format(total_investment))

    if df['Jaar'].iloc[-1] == earliest_investment:
        vorige_jaren = 'De investering gebeurde voor de eerste gepubliceerde cijfers'
    else:
        earlier_df = df[df['Jaar'] < earliest_investment]
        vorige_jaren = earlier_df

    latere_jaren = df[df['Jaar'] >= earliest_investment]
    cijfer_df = normal_df.loc['{}'.format(bedrijf)]
    cijfer_df = cijfer_df.loc[:, cijfer_df.any()]  # don't show columns that only have 0 values

    # cijfer_df.set_index('Jaar', inplace=True)
    return (bedrijf_ouput,
            participatie_output,
            lening_tekst,
            lening_output,
            geinvesteerd_bedrag,
            investeringsjaar,
            vorige_jaren,
            latere_jaren,
            cijfer_df,
            investeringen_aangepast
            )


def ratio_outputs(firm):
    bedrijf = firm.upper()
    ratio_list = ['Jaar', 'Current Ratio', 'Quick Ratio', 'Rendabiliteit bedrijfsactiva',
                  'Brutorendabiliteit totale activa',
                  'Nettorendabiliteit totale activa', 'Nettorendabiliteit eigen vermogen',
                  'Financiële onafhankelijkheid',
                  'Financieringsstabiliteit', 'Aflossingscapaciteit', 'NBK', 'Nettothesaurie'
                  ]
    ratio_output = ratio_df.loc['{}'.format(bedrijf)]
    ratio_output = ratio_output[ratio_list]
    ratio_output = ratio_output.round(2)
    return ratio_output


# * Grafieken
def grafieken(firm):
    df = ratio_outputs(firm)
    jaren = investeringsoutputs(firm)[9]

    fig1 = go.Figure()
    fig1.add_scatter(x=df['Jaar'], y=df['Current Ratio'], name="Current Ratio")
    fig1.add_scatter(x=df['Jaar'], y=df['Quick Ratio'], name="Quick Ratio")
    fig1.add_shape(type="line", line_color="black", line_width=3, opacity=.5, line_dash="dot",
                   x0=0, x1=1, xref="paper", y0=1, y1=1,
                   )

    for i in jaren:
        fig1.add_vline(x=i, line_width=1, line_dash="dash", line_color="green")

    fig1.update_layout(title='Liquiditeit',
                       title_x=0.5,
                       template="simple_white",
                       )
    fig1.update_xaxes(tickmode='array',
                      tickvals=df['Jaar'],
                      )

    fig2 = go.Figure()
    fig2.add_scatter(x=df['Jaar'], y=df['Rendabiliteit bedrijfsactiva'], name="rend. BA ")
    fig2.add_scatter(x=df['Jaar'], y=df['Brutorendabiliteit totale activa'], name="brutorend. TA")
    fig2.add_scatter(x=df['Jaar'], y=df['Nettorendabiliteit totale activa'], name="nettorend. TA")

    for i in jaren:
        fig2.add_vline(x=i, line_width=1, line_dash="dash", line_color="green")

    fig2.update_layout(title='Rendabiliteit',
                       title_x=0.5,
                       template="simple_white",
                       )
    fig2.update_xaxes(tickmode='array',
                      tickvals=df['Jaar'],
                      )

    fig3 = go.Figure()
    fig3.add_scatter(x=df['Jaar'], y=df['Financiële onafhankelijkheid'], name="fin. onafh. ")
    fig3.add_scatter(x=df['Jaar'], y=df['Financieringsstabiliteit'], name="fin. stab.")
    fig3.add_scatter(x=df['Jaar'], y=df['Aflossingscapaciteit'], name="afloss. cap.")

    fig3.add_shape(type="line", line_color="black", line_width=3, opacity=.5, line_dash="dot",
                   x0=0, x1=1, xref="paper", y0=0, y1=0,
                   )

    for i in jaren:
        fig3.add_vline(x=i, line_width=1, line_dash="dash", line_color="green")

    fig3.update_layout(title='Financiële Structuur',
                       title_x=0.5,
                       template="simple_white",
                       )
    fig3.update_xaxes(tickmode='array',
                      tickvals=df['Jaar'],
                      )

    return fig1, fig2, fig3

def average_portfolio():
    unique_years = ratio_df['Jaar'].unique().tolist()

    average_list = []
    for year in unique_years:
        yearly_df = ratio_df[ratio_df['Jaar'] == year]
        average_list.append(yearly_df.mean())

    average_df = pd.DataFrame(average_list).round(2)
    average_df.Jaar = pd.to_datetime(average_df.Jaar, format='%Y').dt.year
    average_df.set_index('Jaar', inplace=True, drop=True)

    return average_df



investeringen = investeringsoutputs(firm)
print(investeringen)