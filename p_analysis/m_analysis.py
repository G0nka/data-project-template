
# analysis functions

def analyze(df):
    grouped_df = df[['uuid', 'Country', 'Job Title', 'Age Group']].groupby(
        ['Country', 'Job Title', 'Age Group']).count()
    grouped_df.rename(columns={'uuid': 'Quantity'}, inplace=True)
    grouped_df['Percentage'] = grouped_df.groupby(level=0).transform(lambda x: x / x.sum())
    grouped_df = grouped_df.reset_index()
    return grouped_df
