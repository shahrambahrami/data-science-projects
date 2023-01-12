#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: shahram
"""

import pandas as pd

df = pd.read_csv('glassdoor_jobs_raw.csv')

df = df[df['Salary Estimate'] != '-1']

df['hourly'] = df['Salary Estimate'].apply(lambda x: 1 if 'per hour' in x.lower() else 0)
df['employer_provided'] = df['Salary Estimate'].apply(lambda x: 1 if 'employer provided salary:' in x.lower() else 0)
salary_estimate = df['Salary Estimate'].apply(lambda x: x.split('(')[0])
minus_dollar_k = salary_estimate.apply(lambda x: x.replace('K', '').replace('$', ''))
minus_hour_salary = minus_dollar_k.apply(lambda x: x.lower().replace('per hour', '').replace('employer provided salary:', ''))

df['min_salary'] = minus_hour_salary.apply(lambda x: int(x.split('-')[0]))
df['max_salary'] = minus_hour_salary.apply(lambda x: int(x.split('-')[1]))
df['avg_salary'] = (df['min_salary'] + df['max_salary']) / 2

df['company_name'] = df.apply(lambda x: x['Company Name'] if x['Rating'] < 0 else x['Company Name'][:-3], axis=1)
df['job_state'] = df['Location'].apply(lambda x: x.lower().split(',')[1])
df['same_state'] = df.apply(lambda x: 1 if x['Location'] == x['Headquarters'] else 0, axis=1)
df['company_age'] = df['Founded'].apply(lambda x: x if x<1 else 2022-x)
df['python'] = df['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)


df['r'] = df['Job Description'].apply(lambda x: 1 if 'r studio' in x.lower() or 'r-studio' in x.lower() else 0)
df['spark'] = df['Job Description'].apply(lambda x: 1 if 'spark' in x.lower() else 0)
df['aws'] = df['Job Description'].apply(lambda x: 1 if 'aws' in x.lower() else 0)
df['excel'] = df['Job Description'].apply(lambda x: 1 if 'excel' in x.lower() else 0)

df_cleaned = df.drop(['Unnamed: 0'], axis=1)
df_cleaned.to_csv('dataset_cleaned.csv', index=False)