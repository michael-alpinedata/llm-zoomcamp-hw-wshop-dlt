import duckdb

con = duckdb.connect("agent_traces.duckdb")

con.sql("""
    SELECT column_name 
    FROM information_schema.columns 
    WHERE table_schema = 'agent_traces_data' 
      AND table_name = 'traces'
      AND column_name ILIKE '%token%'
""").show()

con.sql("""
    SELECT trace_id, span_name, start_timestamp 
    FROM agent_traces_data.traces 
    ORDER BY start_timestamp DESC
""").show()

con.sql("""
    SELECT SUM(attributes__gen_ai_usage_input_tokens) AS total_input_tokens
    FROM agent_traces_data.traces
    WHERE trace_id = '019f6cf99c6c7da442180139f73985b4'
      AND span_name LIKE 'chat%'
""").show()