import dash
from dash import dcc
from dash import html
from dash import dash_table
import dash_bootstrap_components as dbc


from dash.dependencies import Input, Output

from functions import investeringsoutputs, ratio_outputs, grafieken


#######################################################################################################################
# ! Algemene informatie tab
#######################################################################################################################
def register_callbacks_info(app):
    @app.callback(Output('bedrijfsnaam', 'children'), [Input('dropdown', 'value')])
    def participatie_info(input):
        bedrijf_output = investeringsoutputs(input)[0]
        return bedrijf_output

    @app.callback(Output('participatie', 'children'), [Input('dropdown', 'value')])
    def participatie_info(input):
        participatie_info = investeringsoutputs(input)[1]
        return participatie_info

    @app.callback(Output('lening_tekst', 'children'), [Input('dropdown', 'value')])
    def participatie_info(input):
        lening_tekst = investeringsoutputs(input)[2]
        return lening_tekst

    @app.callback(Output('lening_table', 'children'), [Input('dropdown', 'value')])
    def participatie_info(input):
        df = investeringsoutputs(input)[3]
        table = dash_table.DataTable(
            id='lening_df',
            data=df.to_dict('records'),
            columns=[{"name": i, "id": i} for i in df.columns],
            # fixed_columns={'headers': True, 'data': 1},
            # sort_action='native',
            style_cell={
                # all three widths are needed
                'minWidth': '50px',
                'textAlign': 'center',
                'overflow': 'hidden', 'font_family': 'nunito sans'
            },
            style_header=
            {'textAlign': 'center',
             'backgroundColor': '#e1861b',
             'fontWeight': 'bold',
             'color': 'white',
             },
            style_as_list_view=True,
            # css=[{'selector': '.dash-cell div.dash-cell-value',
            #       'rule': 'display: inline; white-space: inherit; overflow: hidden; text-overflow: hidden;'}],
        )
        return table

    @app.callback(Output('geinvesteerd_bedrag', 'children'), [Input('dropdown', 'value')])
    def participatie_info(input):
        investering = investeringsoutputs(input)[4]
        return investering

    @app.callback(Output('cijfer_table', 'children'), [Input('dropdown', 'value')])
    def cijferdf_info(input):
        df = investeringsoutputs(input)[8]
        table1 = dash_table.DataTable(
            id='cijfer_df',
            data=df.to_dict('records'),
            columns=[{"name": i, "id": i} for i in df.columns],
            fixed_columns={'headers': True, 'data': 1},
            sort_action='native',
            style_table={'overflowX': 'auto', 'minWidth': '100%', },
            style_cell={
                # all three widths are needed
                'minWidth': '100px',
                'textAlign': 'center',
                'overflow': 'hidden',
                'font_family': 'nunito sans'
            },
            style_header=
            {'textAlign': 'center',
             'backgroundColor': '#e1861b',
             'fontWeight': 'bold',
             'color': 'white',
             },
            style_data_conditional=
            # * Background color of cells
            [{'if': {'row_index': 'odd'}, 'backgroundColor': '#F2F2F2'}],
            style_as_list_view=False,
            css=[{'selector': '.dash-cell div.dash-cell-value',
                  'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'}],
        )
        return table1

    #######################################################################################################################
    # ! Ratio's tab
    ######################################################################################################################
    @app.callback(Output('ratio_table', 'children'), [Input('dropdown', 'value')])
    def ratiodf_info(input):
        df = ratio_outputs(input)
        table2 = dash_table.DataTable(
            id='ratio_df',
            data=df.to_dict('records'),
            columns=[{"name": i, "id": i} for i in df.columns],
            fixed_columns={'headers': True, 'data': 1},
            sort_action='native',
            style_table={'overflowX': 'auto', 'minWidth': '100%', },
            style_cell={
                # all three widths are needed
                # 'minWidth': '160px', 'width': '160px', 'maxWidth': '160px',
                'minWidth': '100px',
                'textAlign': 'center',
                'overflow': 'hidden',
                'font_family': 'nunito sans'
            },
            style_header={
                'textAlign': 'center',
                'backgroundColor': '#e1861b',
                'fontWeight': 'bold',
                'color': 'white',
            },
            style_data_conditional=
            # * Background color of cells
            [{'if': {'row_index': 'odd'}, 'backgroundColor': '#F2F2F2'}]

            # * Data color of cells
            + [{'if': {'filter_query': '{Current Ratio} > 1 && {Current Ratio} < 1.5', 'column_id': 'Current Ratio'},
                'color': '#208b3a'}]
            + [{'if': {'filter_query': '{Current Ratio} < 1 or {Current Ratio} > 1.5', 'column_id': 'Current Ratio'},
                'color': '#bc4749'}]
            + [{'if': {'filter_query': '{Quick Ratio} > 1', 'column_id': 'Quick Ratio'},
                'color': '#208b3a'}]
            + [{'if': {'filter_query': '{Quick Ratio} < 1', 'column_id': 'Quick Ratio'},
                'color': '#bc4749'}]
             + [{'if': {'filter_query': '{Rendabiliteit bedrijfsactiva} > 0', 'column_id': 'Rendabiliteit bedrijfsactiva'},
                'color': '#208b3a'}]
             + [{'if': {'filter_query': '{Rendabiliteit bedrijfsactiva} < 0', 'column_id': 'Rendabiliteit bedrijfsactiva'},
                'color': '#bc4749'}]
             + [{'if': {'filter_query': '{Brutorendabiliteit totale activa} > 0',
                        'column_id': 'Brutorendabiliteit totale activa'},
                 'color': '#208b3a'}]
             + [{'if': {'filter_query': '{Brutorendabiliteit totale activa} < 0',
                        'column_id': 'Brutorendabiliteit totale activa'},
                 'color': '#bc4749'}]
             + [{'if': {'filter_query': '{Nettorendabiliteit totale activa} > 0',
                        'column_id': 'Nettorendabiliteit totale activa'},
                 'color': '#208b3a'}]
             + [{'if': {'filter_query': '{Nettorendabiliteit totale activa} < 0',
                        'column_id': 'Nettorendabiliteit totale activa'},
                 'color': '#bc4749'}]
            + [{'if': {'filter_query': '{Nettorendabiliteit eigen vermogen} > 0',
                       'column_id': 'Nettorendabiliteit eigen vermogen'},
                'color': '#208b3a'}]
            + [{'if': {'filter_query': '{Nettorendabiliteit eigen vermogen} < 0',
                       'column_id': 'Nettorendabiliteit eigen vermogen'},
                'color': '#bc4749'}]


            ,
            style_as_list_view=False,
            css=[{'selector': '.dash-cell div.dash-cell-value',
                  'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'}],
        )
        return table2

    #######################################################################################################################
    # ! Grafieken tab
    ######################################################################################################################
    @app.callback(Output('liquiditeitsgraph', 'figure'), [Input('dropdown', 'value')])
    def liq_graph(input):
        fig = grafieken(input)[0]
        return fig

    @app.callback(Output('rendabiliteitsgraph', 'figure'), [Input('dropdown', 'value')])
    def rend_graph(input):
        fig = grafieken(input)[1]
        return fig

    @app.callback(Output('structuurgraph', 'figure'), [Input('dropdown', 'value')])
    def structuur_graph(input):
        fig = grafieken(input)[2]
        return fig

