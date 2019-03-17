import pandas as pd
#from sqlalchemy import create_engine

file = '/scratch/Second_analysis_proteingo/contacts_second_paper/is_hb.csv'

lines = pd.read_csv(file, nrows=10000)

print (lines)