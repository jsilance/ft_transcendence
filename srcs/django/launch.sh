
DB_HOST="db"
DB_PORT="5432"

while true;
do
	PGPASSWORD=$POSTGRES_PASSWORD psql -h "$DB_HOST" -p "$DB_PORT" -d "$POSTGRES_DB" -U "$POSTGRES_USER" -c "SELECT 1;" 2>/dev/null 1>/dev/null;
	if [ $? -eq 0 ]; then
		break
	fi
done

# wget https://github.com/mrdoob/three.js/archive/master.zip
# unzip master.zip
# mv three.js-master threejs
# rm master.zip

if [ $? -eq 0 ]; then
    echo "La connexion à la base de données PostgreSQL est réussie.";
	python3 -m pip install daphne;
	python3 manage.py makemigrations;
	python3 manage.py migrate;
	python3 manage.py runserver 0.0.0.0:8000;
else
    echo "Échec de la connexion à la base de données PostgreSQL.";
fi
