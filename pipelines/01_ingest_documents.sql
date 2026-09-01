-- Example Bronze ingestion target.
CREATE TABLE IF NOT EXISTS ${catalog}.${schema}.energy_docs_bronze (
  document_id STRING,
  path STRING,
  content BINARY,
  ingest_ts TIMESTAMP
);
