CREATE DATABASE ft_trans;
CREATE USER skinner WITH PASSWORD 'kappa';
ALTER ROLE skinner SET client_encoding TO 'utf8';
ALTER ROLE skinner SET default_transaction_isolation TO 'read committed';
ALTER ROLE skinner SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE ft_trans TO skinner;
