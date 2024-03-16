import pandas as pd
import redshift_connector
conn = redshift_connector.connect(
    host='data-analysis-staging-staging1.cgrrbmzkztxz.us-east-1.redshift.amazonaws.com',
    database='data',
    port=5439,
    user='gen_ai_hrs',
    password='HrSData1'
)

query = """select t.table_schema, t.table_name
from information_schema.tables t
where t.table_schema = 'gen_ai_hrs_data'"""

# query = """select * from gen_ai_hrs_data.patient_list; """

df = pd.read_sql(query, conn)
pd.set_option('display.max_columns', None)
print(df)
