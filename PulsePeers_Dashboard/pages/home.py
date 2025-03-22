from dash import html, dcc, callback, register_page
from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import numpy as np
from Helpers import Read_Clean_Data, plot_vertical_bar


register_page(
    __name__,
    path='/',  # This is the URL path
    name='Parent Concern',  # This is the name that appears in navbar
    title='Parent Concern'  # This appears in browser tab
)


# Read and clean data for
fdir = '/Users/clarechao/code/python/PulsePeers/data'
fname_parents = f'{fdir}/Pulse_Parents_Survey_CChao.csv'
# fname_parents = 'Pulse_Parents_Survey_CChao.csv'
df_parents = Read_Clean_Data(fname_parents)

layout = dbc.Container([
    html.H1(id='pc-title', style={"text-align": "center"}),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dcc.Markdown("""Select a **State**:""",
                             className='text-primary markdown-font'
                             ),
                dcc.Dropdown(
                    id='state-dropdown',
                    options=df_parents['State'].dropna().unique().tolist() + ['All'],
                    value='All'
                ),
                html.Br(),
                dcc.Markdown('Select a **Age Group**:',
                             className = 'text-primary markdown-font'),
                dcc.Dropdown(
                    id='agegrp-dropdown',
                    options=df_parents['Age'].dropna().unique().tolist() + ['All'],
                    value='All',
                ),
                html.Br(),
                dcc.Markdown('Select a **Gender**:',
                             className = 'text-primary markdown-font'),
                dcc.Dropdown(
                    id='gender-dropdown',
                    options=df_parents['Gender'].dropna().unique().tolist() + ['All'],
                    value='All',
                ),
                html.Br(),
                dcc.Markdown('Select a **Marital Status**:',
                             className = 'text-primary markdown-font'),
                dcc.Dropdown(
                    id='maritalstatus-dropdown',
                    options=df_parents['Marital Status'].dropna().unique().tolist() + ['All'],
                    value='All',
                ),
                html.Br(),
                dcc.Markdown('Select a **Ethnicity**:',
                             className = 'text-primary markdown-font'),
                dcc.Dropdown(
                    id='ethnicity-dropdown',
                    options=df_parents['Ethnicity'].dropna().unique().tolist() + ['All'],
                    value='All',
                ),
                html.Br(),
                dcc.Markdown('Select a **# of Teens in the Family**:',
                             className = 'text-primary markdown-font'),
                dcc.Dropdown(
                    id='numofteens-dropdown',
                    options=np.sort(df_parents['NumofTeens'].dropna().unique()).tolist() + ['All'],
                    value='All',
                ),
                # html.Br(),
                # dcc.Markdown('Select a **Level of Parent Involvement in Teen**\'s life:',
                #              className = 'text-primary markdown-font'),
                # dcc.Dropdown(
                #     id='parentinvolve-dropdown',
                #     options=np.sort(df_parents['Parent_Involve'].dropna().unique()).tolist() + ['All'],
                #     value='All',
                # ),
                # html.Br(),
                # dcc.Markdown('Select a **Comfort Level of the Teen Sharing with Parents**',
                #              className = 'text-primary markdown-font'),
                # dcc.Dropdown(
                #     id='teenshare-dropdown',
                #     options=np.sort(df_parents['Teen_Share'].dropna().unique()).tolist() + ['All'],
                #     value='All',
                # )
            ])
        ], width=3),
        dbc.Col([
            dcc.Graph(id='pc_vbar')
        ], width=9)
    ],align="center", className="mb-4")
], fluid=True)

@callback(
    [Output('pc-title', 'children'),
    Output('pc_vbar', 'figure')],
    [Input('state-dropdown', "value"),
    Input('agegrp-dropdown', "value"),
    Input('gender-dropdown', "value"),
    Input('maritalstatus-dropdown', "value"),
    Input('ethnicity-dropdown', 'value'),
    Input('numofteens-dropdown', 'value')]
    #Input('parentinvolve-dropdown', 'value'),
    # Input('teenshare-dropdown', 'value')]
)
# def plot_pc_vbar(state, agegrp, gender, marrysts, ethnicity, numofteens, parentinvolve, teenshare):
def plot_pc_vbar(state, agegrp, gender, marrysts, ethnicity, numofteens):
    if not state and agegrp and gender and marrysts and ethnicity and numofteens:
        raise PreventUpdate

    # filter out the right data first
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
    # if parentinvolve != 'All':
    #     title = title + f' Parent Involve level {parentinvolve}'
    #     df_filter = df_filter.query('Parent_Involve == @parentinvolve')
    # if teenshare != 'All':
    #     title = title + f' Teen Sharing level {teenshare}'
    #     df_filter = df_filter.query('Teen_Share == @teenshare')
    title = title + ' Concerned About?'


    cols_pc = [ss for ss in df_filter.columns if ss.startswith('PC_')]
    df_pc = df_filter[cols_pc].mean().sort_values(ascending=False).reset_index()
    df_pc.columns = ['Parent Concern Category', '% Total']
    pc_cat_order = df_pc['Parent Concern Category'].tolist()

    # make yaxislabel dictionary for the right label
    yylabel_values = [ss.removeprefix('PC_') for ss in cols_pc]
    yylabel_dct = dict(zip(cols_pc, yylabel_values))

    # plot vbar fig
    fig = plot_vertical_bar(df_pc,
                      '% Total',
                      'Parent Concern Category',
                      '% Total',
                      '.0%',
                      {'Parent Concern Category': pc_cat_order})

    return title, fig