import pandas as pd
import pyarrow.parquet as pq
import duckdb
import pyarrow as pa

def Writing(datas):
    df = pd.DataFrame(datas)
    table = pa.Table.from_pandas(df)
    pq.write_table(table, 'test.parquet')
    # con = duckdb.connect(database='test.db')
    # con.execute("CREATE TABLE events (name VARCHAR(80), date VARCHAR(10), "
    #             "time VARCHAR(10), href VARCHAR(200), img VARCHAR(200)) ")
    # con.execute("INSERT INTO ")
    con = duckdb.connect(database='test.db', read_only=False)
    con.execute("CREATE TABLE test (name VARCHAR(80), date VARCHAR(10), "
                 "time VARCHAR(10), href VARCHAR(200), img VARCHAR(200))")
    table = pq.read_table('test.parquet')
    df = table.to_pandas()
    con.register('test', df)
    print(con.execute("SELECT * FROM test").fetchdf())