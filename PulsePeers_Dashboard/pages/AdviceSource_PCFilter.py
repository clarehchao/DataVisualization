from dash import html, dcc, callback, register_page
from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import numpy as np
from Helpers import Read_Clean_Data, plot_vertical_bar


register_page(
    __name__,
    path='/AdviceSource_PCFilter',
    name='Cross-filtered Advice Source',
    title='The Source of Advice that Parents Seek'
)

# Read and clean data for
fdir = '/Users/clarechao/code/python/PulsePeers/data'
fname_parents = f'{fdir}/Pulse_Parents_Survey_CChao.csv'
# fname_parents = 'Pulse_Parents_Survey_CChao.csv'
df_parents = Read_Clean_Data(fname_parents)

arial_style = {
    'fontFamily': 'Arial, sans-serif'
}

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dcc.Markdown("""Select a **State**:""",
                             className='text-primary fs-7',
                             style=arial_style
                             ),
                # html.P('Select a State:', style={'font-family': 'Arial', 'font-weight': 'bold'}),
                dcc.Dropdown(
                    id='state-dropdown2',
                    options=df_parents['State'].dropna().unique().tolist() + ['All'],
                    value='All'
                )])
        ]),
        dbc.Col([
            dbc.Card([
                dcc.Markdown('Select a **Age Group**:',
                             className='text-primary fs-7',
                             style=arial_style
                             ),
                dcc.Dropdown(
                    id='agegrp-dropdown2',
                    options=df_parents['Age'].dropna().unique().tolist() + ['All'],
                    value='All'
                )
            ])
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dcc.Markdown('Select a **Gender**:',
                             className='text-primary fs-7',
                             style=arial_style),
                dcc.Dropdown(
                    id='gender-dropdown2',
                    options=df_parents['Gender'].dropna().unique().tolist() + ['All'],
                    value='All',
                )
            ])
        ]),
        dbc.Col([
            dbc.Card([
                dcc.Markdown('Select a **Marital Status**:',
                             className='text-primary fs-7',
                             style=arial_style
                             ),
                dcc.Dropdown(
                    id='maritalstatus-dropdown2',
                    options=df_parents['Marital Status'].dropna().unique().tolist() + ['All'],
                    value='All',
                )
            ])
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dcc.Markdown('Select a **Ethnicity**:',
                             className='text-primary fs-7',
                             style=arial_style
                             ),
                dcc.Dropdown(
                    id='ethnicity-dropdown2',
                    options=df_parents['Ethnicity'].dropna().unique().tolist() + ['All'],
                    value='All'
                )
            ])
        ]),
        dbc.Col([
            dbc.Card([
                dcc.Markdown('Select a **# of Teens in the Family**:',
                             className='text-primary fs-7',
                             style=arial_style
                             ),
                dcc.Dropdown(
                    id='numofteens-dropdown2',
                    options=np.sort(df_parents['NumofTeens'].dropna().unique()).tolist() + ['All'],
                    value='All',
                )
            ])
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.H5(id='pc-title2', style={"text-align": "center"}),
            dcc.Graph(id='cross-filter-pc-vbar',
                      hoverData={'points': [{'customdata': ['PC_Communication']}]}),
        ]),
        dbc.Col([
            html.H5(id='adsrc-title', style={"text-align": "center"}),
            dcc.Graph(id='adsrc-vbar')
        ])
    ])
])

@callback(
    Output('pc-title2', 'children'),
    Output('cross-filter-pc-vbar', 'figure'),
    Input('state-dropdown2', "value"),
    Input('agegrp-dropdown2', "value"),
    Input('gender-dropdown2', "value"),
    Input('maritalstatus-dropdown2', "value"),
    Input('ethnicity-dropdown2', 'value'),
    Input('numofteens-dropdown2', 'value'),
)
def plot_pc_vbar(state, agegrp, gender, marrysts, ethnicity, numofteens):
    if not state and agegrp and gender and marrysts and ethnicity and numofteens:
        raise PreventUpdate
    # filter out the right data first
    # title = 'What are parents concerned about?'
    title = 'What are '
    df_filter = df_parents

    if marrysts != 'All':
        title = title + f'{marrysts}'
        df_filter = df_filter.query('`Marital Status` == @marrysts')
    if gender != 'All':
        title = title + f' {gender}'
        df_filter = df_filter.query('Gender == @gender')
    if agegrp != 'All':
        title = title + f' {agegrp} y.o'
        df_filter = df_filter.query('Age == @agegrp')
    if ethnicity != 'All':
        title = title + f' {ethnicity}'
        df_filter = df_filter.query('Ethnicity == @ethnicity')

    title = title + ' Parents '

    if state != 'All':
        title = title + f'in {state}'
        df_filter = df_filter.query('State == @state')
    if numofteens != 'All':
        title = title + f' with {numofteens}'
        if numofteens > 1:
            title = title + ' Teens in family'
        else:
            title = title + ' Teen in family'
        df_filter = df_filter.query('NumofTeens == @numofteens')

    title = title + ' Concerned About?'
    # cols_pc = ['PC_Career And Academic Development', 'PC_Communication',
    #            'PC_Excessive Technology Use', 'PC_Healthy Boundaries',
    #            'PC_Identity Development', 'PC_Life Balance',
    #            'PC_Mental Health Well-Being', 'PC_Normal Growing Pains', 'PC_Nothing',
    #            'PC_Other', 'PC_Social Challenges', 'PC_Substance Abuse & Self-Harm']

    cols_pc = [ss for ss in df_filter.columns if ss.startswith('PC_')]
    print(cols_pc)
    df_pc = df_filter[cols_pc].mean().sort_values(ascending=False).reset_index()
    df_pc.columns = ['Parent Concern Category', '% Total']
    pc_cat_order = df_pc['Parent Concern Category'].tolist()

    # make yaxislabel dictionary for the right label
    yylabel_values = [ss.removeprefix('PC_') for ss in cols_pc]
    yylabel_dct = dict(zip(cols_pc, yylabel_values))

    fig = plot_vertical_bar(df_pc,
                            '% Total',
                            'Parent Concern Category',
                            '% Total',
                            '.0%',
                            {'Parent Concern Category': pc_cat_order},
                            wd=600,
                            ht=600,
                            hovername='Parent Concern Category',
                            customdata=['Parent Concern Category'],
                            ylabeldct=yylabel_dct)
    print(f'in pc_var: {title}')
    return title, fig


@callback(
    Output('adsrc-title', 'children'),
    Output('adsrc-vbar', 'figure'),
    Input('cross-filter-pc-vbar', 'hoverData'),
    Input('state-dropdown2', "value"),
    Input('agegrp-dropdown2', "value"),
    Input('gender-dropdown2', "value"),
    Input('maritalstatus-dropdown2', "value"),
    Input('ethnicity-dropdown2', 'value'),
    Input('numofteens-dropdown2', 'value'),
)
def update_ad(hoverData, state, agegrp, gender, marrysts, ethnicity, numofteens):
    if not hoverData and state and agegrp and gender and marrysts and ethnicity and numofteens:
        raise PreventUpdate

    pc_cat = hoverData["points"][0]["customdata"][0]
    df_filter = df_parents.query(f'`{pc_cat}` == 1')

    title = 'What Source of Advice do '
    if marrysts != 'All':
        title = title + f'{marrysts}'
        df_filter = df_filter.query('`Marital Status` == @marrysts')
    if gender != 'All':
        title = title + f' {gender}'
        df_filter = df_filter.query('Gender == @gender')
    if agegrp != 'All':
        title = title + f' {agegrp} y.o'
        df_filter = df_filter.query('Age == @agegrp')
    if ethnicity != 'All':
        title = title + f' {ethnicity}'
        df_filter = df_filter.query('Ethnicity == @ethnicity')

    title = title + ' Parents '

    if state != 'All':
        title = title + f'in {state}'
        df_filter = df_filter.query('State == @state')
    if numofteens != 'All':
        title = title + f' with {numofteens}'
        if numofteens > 1:
            title = title + ' Teens in family'
        else:
            title = title + ' Teen in family'
        df_filter = df_filter.query('NumofTeens == @numofteens')

    title = title + ' seek?'

    # cols_adcsrc = ['AdS_A.I.', 'AdS_Books', 'AdS_Families & Friends',
    #                'AdS_Online Resources', 'AdS_Other Parents',
    #                'AdS_Religious & Spiritual Community', 'AdS_School',
    #                'AdS_Therapist & Professionals']
    cols_adcsrc = [ss for ss in df_filter.columns if ss.startswith('AdS_')]
    print(cols_adcsrc)
    df_advsrc = df_filter[cols_adcsrc].mean().sort_values(ascending=False).reset_index()
    df_advsrc.columns = ['Advice Source Category', '% Total']
    advsrc_cat_order = df_advsrc['Advice Source Category'].tolist()

    # make yaxislabel dictionary for the right label
    yylabel_values = [ss.removeprefix('AdS_') for ss in cols_adcsrc]
    yylabel_dct = dict(zip(cols_adcsrc, yylabel_values))

    fig = plot_vertical_bar(df_advsrc,
                            '% Total',
                            'Advice Source Category',
                            '% Total',
                            '.0%',
                            {'Advice Source Category': advsrc_cat_order},
                            wd=600,
                            ht=600,
                            hexcolor='#f25c54',
                            ylabeldct=yylabel_dct)

    print(f'in update callback: {title}')

    return title, fig