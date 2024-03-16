from dotenv import load_dotenv
from langchain_community.llms import Bedrock
from langchain.sql_database import SQLDatabase
from sqlalchemy.engine.url import URL
from langchain_experimental.sql import SQLDatabaseChain
from langchain_core.prompts import PromptTemplate

import os
import sqlalchemy as sa


load_dotenv()
llm = Bedrock(
    credentials_profile_name="ravi",
    model_id="mistral.mixtral-8x7b-instruct-v0:1",
    # model_id="amazon.titan-text-express-v1",
    endpoint_url="https://bedrock-runtime.us-west-2.amazonaws.com",
    region_name="us-west-2",
    model_kwargs={"temperature": 0, "max_tokens": 4000},
    verbose=True
)


def nurse_report(question):
    url = URL.create(
        drivername='redshift+redshift_connector',  # indicate redshift_connector driver and dialect will be used
        host=os.getenv('redshift_host'),  # Amazon Redshift host
        port=os.getenv('redshift_port'),  # Amazon Redshift port
        database=os.getenv('redshift_database'),  # Amazon Redshift database
        username=os.getenv('redshift_username'),  # Amazon Redshift username
        password=os.getenv('redshift_password')  # Amazon Redshift password
    )
    engine = sa.create_engine(url)
    db = SQLDatabase(engine, schema='gen_ai_hrs_data', include_tables=['base_medication_data'],
                     sample_rows_in_table_info=3)
    # with engine.connect() as conn:
    #     print(pd.read_sql(sql="select count(*) from gen_ai_hrs_data.clinician_connect", con=conn.connection))
    with open('Data/prompt.txt', 'r') as file:
        context = file.read()
    prompt = PromptTemplate.from_template(context)
    sql_db_chain = SQLDatabaseChain.from_llm(
        llm,
        db,
        use_query_checker=True,
        verbose=True,
        return_intermediate_steps=True,
    )
    answer = sql_db_chain(f"""{question}""")
    # answer = llm.invoke(f"""{context}/n{question}""")
    print(answer)
    return answer['result'], answer['intermediate_steps'][1]
    # with engine.connect() as conn:
    #     df = pd.read_sql(sql=answer, con=conn.connection)
    # pandas_ai = SmartDataframe(df, config={"llm": llm})
    # response = pandas_ai.chat("Summarize this dataframe explaining what the columns are")
    # print(response)
    # return response, answer, df
