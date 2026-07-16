"""pull_logfire_traces.py"""

import os

import dlt
from dotenv import load_dotenv
from logfire.query_client import LogfireQueryClient

load_dotenv()

READ_TOKEN = os.environ["LOGFIRE_READ_TOKEN"]

SQL_QUERY = """
SELECT 
    trace_id,
    span_id,
    span_name,
    start_timestamp,
    duration,
    attributes
FROM records
ORDER BY start_timestamp DESC
"""


@dlt.resource(name="traces", write_disposition="replace")
def logfire_records():
    with LogfireQueryClient(read_token=READ_TOKEN) as client:
        result = client.query_json_rows(sql=SQL_QUERY, limit=10000)
    yield result["rows"]


def load():
    pipeline = dlt.pipeline(
        pipeline_name="agent_traces",
        destination="duckdb",
        dataset_name="agent_traces_data",
    )
    info = pipeline.run(logfire_records())
    print(info)
    print(pipeline.last_trace.last_normalize_info)


if __name__ == "__main__":
    load()