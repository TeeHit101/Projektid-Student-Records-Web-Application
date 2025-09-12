#!/bin/sh
set -e
host="$1"
shift
cmd="$@"

# Vänta tills Postgres accepterar anslutningar
until PGPASSWORD=postgres psql -h "$host" -U "postgres" -d postgres -c '\q'; do
  echo "❌ Väntar på databasen..."
  sleep 2
done

echo "✅ Databas redo!"
exec $cmd
