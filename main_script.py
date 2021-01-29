from p_acquisition import m_acquisition as mac
from p_wrangling import m_wrangling as mwr
from p_analysis import m_analysis as man 
from p_reporting import m_reporting as mre 


def main():
    print('======== Starting pipeline... ========')

    raw_df = mac.acquire()
    final_df = mwr.refine(raw_df)
    analyzed_df = man.analyze(final_df)
    mre.print_csv(analyzed_df)

    print('Results saved in folder ./data/results')
    print('======== Pipeline is complete! ========')


if __name__ == '__main__':
    main()
