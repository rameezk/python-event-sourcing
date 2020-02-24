test:
	python -m unittest *_test.py;

run:
	docker-compose up;

stop:
	docker-compose stop;

migrate:
	psql -a -f database.sql

run-detached:
	docker-compose up -d;

clean:
	docker-compose stop; docker-compose rm -f;
