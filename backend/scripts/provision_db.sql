-- ============================================================================
--  NutriAI Fit — Provisionamento do banco (RODE UMA VEZ, como superusuário)
-- ----------------------------------------------------------------------------
--  Por que este arquivo existe:
--   - O aplicativo NUNCA deve se conectar como o superusuário 'postgres'.
--     Se a credencial do app vazar, o estrago fica limitado a um único banco.
--   - Aqui criamos uma ROLE dedicada de MENOR PRIVILÉGIO ('nutriai') e um
--     banco próprio ('nutriai_fit') do qual essa role é dona.
--   - Este arquivo (com a senha real) está no .gitignore. A versão versionada
--     é provision_db.example.sql, com um placeholder.
--
--  Como rodar (PowerShell):
--   & "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -f backend\scripts\provision_db.sql
--   (digite a senha do superusuário 'postgres' quando solicitado)
-- ============================================================================

-- 1) Role da aplicação: pode logar, mas NÃO é superusuário e não cria
--    outros bancos nem outras roles. Privilégio mínimo.
DO
$$
BEGIN
   IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'nutriai') THEN
      CREATE ROLE nutriai
         LOGIN
         PASSWORD '731f38341e5dd012d810ee02e5e3ca35'
         NOSUPERUSER
         NOCREATEDB
         NOCREATEROLE;
   END IF;
END
$$;

-- 2) Banco da aplicação, de posse da role 'nutriai'.
--    CREATE DATABASE não pode rodar dentro de um bloco DO/transação,
--    então usamos o truque do \gexec do psql para torná-lo idempotente.
SELECT 'CREATE DATABASE nutriai_fit OWNER nutriai'
WHERE NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'nutriai_fit')\gexec

-- 3) Trava o schema público dentro do banco: só a role 'nutriai' opera nele.
\connect nutriai_fit
REVOKE ALL ON SCHEMA public FROM PUBLIC;
ALTER SCHEMA public OWNER TO nutriai;
GRANT ALL ON SCHEMA public TO nutriai;

-- Pronto. O Alembic (rodando como 'nutriai') criará as tabelas neste banco.
-- Melhoria futura: separar uma role só de migração (DDL) de uma role de
-- runtime (apenas SELECT/INSERT/UPDATE/DELETE) para reduzir ainda mais a superfície.
