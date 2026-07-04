-- Runs once, on first container init, against the default POSTGRES_DB.
-- Creates the two logical databases used by the stack and enables pgvector
-- on cognee_db (cognee's vector store).

CREATE DATABASE cognee_db;
CREATE DATABASE hindsight_app;

\connect cognee_db
CREATE EXTENSION IF NOT EXISTS vector;
