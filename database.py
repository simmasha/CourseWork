# import pandas as pd
# import pyarrow as pa
import pyarrow.parquet as pq
import duckdb

def Writing():
    # con = duckdb.connect(database='test.db')
    # con.execute("CREATE TABLE events (name VARCHAR(80), date VARCHAR(10), "
    #             "time VARCHAR(10), href VARCHAR(200), img VARCHAR(200)) ")
    # con.execute("INSERT INTO ")
    con = duckdb.connect(database='test.db', read_only=False)
    con.execute("CREATE TABLE test (name VARCHAR(80), date VARCHAR(10), "
                 "time VARCHAR(10), href VARCHAR(200), img VARCHAR(200))")
    table = pq.read_table('events_file.parquet')
    df = table.to_pandas()
    con.register('test', df)
    print(con.execute("SELECT * FROM test").fetchdf())
