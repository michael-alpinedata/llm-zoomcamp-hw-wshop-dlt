import duckdb

con = duckdb.connect("agent_traces.duckdb")

con.sql("""
    SELECT COUNT(*) FROM information_schema.tables 
    WHERE table_schema = 'agent_traces_data';
""").show(max_width=10000)
