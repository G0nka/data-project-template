
# reporting functions

def print_csv(df):
    df.to_csv('data/results/countries.csv', index=False)
