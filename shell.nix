{ pkgs ? import <nixpkgs> {} }:

with pkgs;

mkShell {
buildInputs = [
    python3
    postgresql
    redis
    # dev dependencies, not needed on prod env
    pipenv
    pre-commit
    git
];

shellHook = ''
export LOCALE_ARCHIVE="${pkgs.glibcLocales}/lib/locale/locale-archive"
export PGDATA=$PWD/.postgres/db/postgres_data
export PGHOST=$PWD/.postgres/db/postgres
export PGPORT=5432
export LOG_PATH=$PWD/.postgres/db/postgres/LOG
export DATABASE_URL="postgresql:///postgres?host=$PGHOST&port=$PGPORT"
export LC_ALL="en_GB.UTF-8"
export LC_MESSAGES="en_GB.UTF-8"
echo $HOSTNAME

# Create directory if need be
if [ ! -d $PGHOST ]; then
mkdir -p $PGHOST
fi
if [ ! -d $PGDATA ]; then
echo 'Initializing postgresql database...'
initdb $PGDATA --auth=trust >/dev/null
fi

pg_ctl restart -l $LOG_PATH -o "-c unix_socket_directories=$PGHOST"
createuser postgres --superuser --createdb

# Create user and database if need be
psql -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = 'macantine'" | grep -q 1 || psql -U postgres -c "CREATE DATABASE macantine"

# Start redis
redis-server &

# Installing python packages
pipenv install
pipenv lock
pipenv sync

# Clean pipenv files
rm Pipfile.lock
rm Pipfile


'';
}
