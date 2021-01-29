import re

# wrangling functions


def fix_age(age):
    if 'years old' in age:
        born_y = 2016 - int(re.sub("[^\d]", "", age))
    else:
        born_y = int(age)
    right_age = 2021 - born_y
    return right_age


def group_age(age):
    if age <= 25:
        age_group = '(18-25)'
    elif age <= 35:
        age_group = '[30-35)'
    elif age <= 45:
        age_group = '[40-45)'
    elif age <= 55:
        age_group = '[45-55)'
    else:
        age_group = '[55-70)'
    return age_group


def refine(df):
    print('Refining data...')
    df['age'] = df.apply(lambda x: fix_age(x['age']), axis=1)
    df['Age Group'] = df.apply(lambda x: group_age(x['age']), axis=1)
    return df
