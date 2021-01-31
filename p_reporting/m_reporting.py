
# reporting functions

def print_csv(df, country):
    df.to_csv(f'data/results/{country}.csv', index=False)
