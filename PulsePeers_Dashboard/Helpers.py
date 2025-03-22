import pandas as pd
import plotly.express as px


parent_concern_dct = {'academic stress': 'Career and Academic Development',
                          'mental health and emotional well-being': 'Mental Health Well-being',
                          'teen emotional wellbeing': 'Mental Health Well-being',
                          'excessive technology and social media use': 'Excessive Technology Use',
                          'nothing concerns me today': 'Nothing',
                          'balance between school, sports, and family': 'Life Balance',
                          'work/life balance': 'Life Balance',
                          'social challenges (bullying, social isolation)': 'Social Challenges',
                          'social issues': 'Social Challenges',
                          'mental health': 'Mental Health Well-being',
                          'mental health wellbeing': 'Mental Health Well-being',
                          'emotional well-being': 'Mental Health Well-being',
                          'substance abuse - self-harm behaviour': 'Substance Abuse & Self-harm',
                          'identity development (peer pressure, gender exploration)': 'Identity Development',
                          }

# AdviceSource1-5: Categories (Therapist & Professionals, Families & Friends, Other Parents, Google, A.I., Online Resources)
advicesrc_categories_dct = {
    'therapists': 'Therapist & Professionals',
    'therapy': 'Therapist & Professionals',
    'therapist': 'Therapist & Professionals',
    'psychologist': 'Therapist & Professionals',
    'psychologists': 'Therapist & Professionals',
    'pediatrician': 'Therapist & Professionals',
    'psicóloga': 'Therapist & Professionals',
    'therapy/professional help': 'Therapist & Professionals',
    'professionals': 'Therapist & Professionals',
    'holistic therapy': 'Therapist & Professionals',
    'husband': 'Families & Friends',
    'family': 'Families & Friends',
    'your partner': 'Families & Friends',
    'friends': 'Families & Friends',
    'friends/family': 'Families & Friends',
    'friends / family': 'Families & Friends',
    'my own parents': 'Families & Friends',
    'siblings': 'Families & Friends',
    'google': 'Online Resources',
    'instagram following lisa damour and other adolescent psychs': 'Online Resources',
    'facebook groups':'Online Resources',
    'podcasts': 'Online Resources',
    'spiritual coach': 'Religious & Spiritual community',
    'religious community': 'Religious & Spiritual community',
    'parenting books': 'Books',
    'other moms': 'Other Parents',
    'couple': 'Other Parents',
    'friends who are also parents': 'Other Parents',
    'friends who are parents': 'Other Parents',
    'other parents/friends': 'Other Parents',
    'chatgpt': 'Artificial Intelligence',
    'a.i': 'Artificial Intelligence'
}

def Read_Clean_Data(fname):

    # return a dataframe with the var_of_interested updated and clean

    the_df = pd.read_csv(fname)

    # Add age columns for future analysis: # of teens, median teen age, age histogram of teens
    df_tmp = the_df.loc[:,['Teen1','Teen2','Teen3','Teen4','Teen5']]
    the_df['NumofTeens'] = df_tmp.count(axis=1)
    the_df['MedianTeenAge'] = df_tmp.median(axis=1, skipna=True)

    # clean and one hot encode PARENT CONCERN
    cols_PC = ['ParentConcern1', 'ParentConcern2', 'ParentConcern3', 'ParentConcern4']
    df_pc = OneHotEncodeCategory(the_df, cols_PC, parent_concern_dct, 'PC_')

    # clean and one hot encode Advice Source
    cols_Adsrc = [f'AdviceSource{n}' for n in range(1,6)]
    df_more = OneHotEncodeCategory(df_pc, cols_Adsrc, advicesrc_categories_dct, 'AdS_')

    return df_more

def OneHotEncodeCategory(df, cols, cat_dct, prefstr):
    # df: the data_frame with all the data
    # cols: column names of interest
    # cat_dct: category dictionary to transform the string data
    # prefstr: prefix string to add to category column name

    # remove leading and trailing space and period
    cols_upd = [f'{ss}_upd' for ss in cols]
    df[cols_upd] = df[cols].apply(lambda x: x.str.strip().str.lower().str.rstrip('.'), axis=0)

    cols_cat = [f'{ss}_category' for ss in cols]
    # Returns x if x (key) doesn't exist but dict[x] if it does via dict.get()
    df[cols_cat] = df[cols_upd].map(lambda x: cat_dct.get(x, x).title() if pd.notna(x) else x)

    # drop all the cols and updated cols to just have the cols that we find to merge back with the orginal data
    df = df.drop(cols_upd, axis=1)

    df['Combined'] = df[cols_cat].apply(lambda row: ', '.join(row.dropna().astype(str)), axis=1)

    # one hot encoding of all Parent concern category into 0/1
    binary_df = df['Combined'].str.get_dummies(sep=', ')
    new_col = [f'{prefstr}{ss}' for ss in binary_df.columns]
    binary_df.columns = new_col

    df_new = pd.concat([df, binary_df], axis=1)
    df_new = df_new.drop(cols_cat + ['Combined'], axis=1)

    return df_new

def plot_vertical_bar(the_df, xx, yy, xx_text, txt_fmt, cat_order, ht=700,wd=1000, hovername=None, customdata=None,hexcolor='#07beb8', ylabeldct=None):
    # plot vertical bar chart via plotly express and return fig

    fig = px.bar(
        data_frame=the_df,
        x=xx,
        y=yy,
        text=xx_text,
        text_auto=txt_fmt,
        category_orders=cat_order,
        height=ht,
        width=wd,
        hover_name=hovername,
        custom_data=customdata,
    )

    fig.update_traces(marker_color=hexcolor)
    fig.update_layout(
        xaxis_title={
            'font': {'size': 12, 'family': 'Arial Black'}
        },
        yaxis_title={
            'font': {'size': 12, 'family': 'Arial Black'}
        },
        xaxis={
            'tickformat': txt_fmt,
        }
    )
    if ylabeldct is not None:
        fig.update_yaxes(labelalias=ylabeldct)

    return fig