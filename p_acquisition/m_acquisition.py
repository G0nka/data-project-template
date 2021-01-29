from sqlalchemy import create_engine
from bs4 import BeautifulSoup
import pandas as pd
import requests


# acquisition functions


def get_db_data():
    # connection string'
    sqlitedb_rel_path = 'data/raw/raw_data_project_m1.db'
    conn_str = f'sqlite:///{sqlitedb_rel_path}'
    engine = create_engine(conn_str)
    print(f'Reading data from {sqlitedb_rel_path}...')

    # Import initial data from the db: uuid , age , countries...
    initial_df = pd.read_sql_query("""
    SELECT personal_info.uuid, normalized_job_code ,age , country_code FROM personal_info
    INNER JOIN country_info ON personal_info.uuid = country_info.uuid
    INNER JOIN career_info ON personal_info.uuid = career_info.uuid;
    """, engine)
    return initial_df


def extract_job_codes(raw_df):
    job_code_unique = raw_df['normalized_job_code'].unique()
    job_code_l = len(job_code_unique)
    print(f'Extracting {job_code_l} job codes from the API...')

    job_titles = {}
    for code in job_code_unique[1:]:
        results = requests.get(f'http://api.dataatwork.org/v1/jobs/{code}').json()
        job = results['title']
        job_titles[code] = job

    job_titles_df = pd.DataFrame(job_titles.items(), columns=['normalized_job_code', 'Job Title'])
    return job_titles_df


def extract_countries_df():
    print('Getting the country codes by Web scraping...')
    url = 'https://ec.europa.eu/eurostat/statistics-explained/index.php/Glossary:Country_codes'
    html = requests.get(url).content
    soup = BeautifulSoup(html, "html.parser")
    table_countries = soup.find('table', {'width': '80%'}).text
    table_countries = table_countries.replace("\n", "")
    table_countries = table_countries.split(")")
    list_countries = [i.split('(') for i in table_countries]
    country_codes_df = pd.DataFrame(list_countries, columns=('Country', 'country_code'))
    return country_codes_df


def acquire():
    initial_df = get_db_data()
    job_codes_df = extract_job_codes(initial_df)
    country_codes_df = extract_countries_df()

    intermediate_df = pd.merge(initial_df,
                               job_codes_df,
                               on='normalized_job_code',
                               how='inner')

    raw_df = pd.merge(intermediate_df,
                      country_codes_df,
                      on='country_code',
                      how='inner')
    print('Ok. All needed info obtained!')
    return raw_df
