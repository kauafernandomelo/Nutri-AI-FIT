-- ============================================================================
--  NutriAI Fit — Provisionamento do banco (TEMPLATE versionado)
-- ----------------------------------------------------------------------------
--  Copie para provision_db.sql, troque <SUA_SENHA_FORTE> por uma senha forte,
--  e use a MESMA senha no DATABASE_URL do seu .env. Depois rode (PowerShell):
--   & "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -f backend\scripts\provision_db.sql
--  O arquivo provision_db.sql (com a senha real) NÃO é versionado (.gitignore).
-- ============================================================================

DO
$$
BEGIN
   IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'nutriai') THEN
      CREATE ROLE nutriai
         LOGIN
         PASSWORD '<SUA_SENHA_FORTE>'
         NOSUPERUSER
         NOCREATEDB
         NOCREATEROLE;
   END IF;
END
$$;

SELECT 'CREATE DATABASE nutriai_fit OWNER nutriai'
WHERE NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'nutriai_fit')\gexec

\connect nutriai_fit
REVOKE ALL ON SCHEMA public FROM PUBLIC;
ALTER SCHEMA public OWNER TO nutriai;
GRANT ALL ON SCHEMA public TO nutriai;
