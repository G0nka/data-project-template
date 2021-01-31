import argparse
from p_acquisition import m_acquisition as mac
from p_wrangling import m_wrangling as mwr
from p_analysis import m_analysis as man 
from p_reporting import m_reporting as mre

def argument_parser():
    parser = argparse.ArgumentParser(description = 'Set chart type')
    parser.add_argument("-c", "--country", help="Country to analyze")
    args = parser.parse_args()
    return args

def filter_c(country, analyzed_df):
    if country == "All":
        filtered_country_df = analyzed_df
    else:
        filtered_country_df = analyzed_df[analyzed_df['Country']== country]
    return filtered_country_df

def main(country):
    print('======== Starting pipeline... ========')

    raw_df = mac.acquire()
    final_df = mwr.refine(raw_df)
    analyzed_df = man.analyze(final_df)
    filtered_df = filter_c(country, analyzed_df)
    mre.print_csv(filtered_df, country)

    print(f'Results for {country} saved in folder ./data/results')
    print('======== Pipeline is complete! ========')


if __name__ == '__main__':
    country = str(input('Please enter the country (for a complete list enter "All"): '))
    arguments = argument_parser()
    main(country)
