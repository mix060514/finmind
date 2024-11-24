create-mysql:
	docker compose -f mysql.yml up -d

close-mysql:
	docker compose -f mysql.yml down

create-rabbitmq:
	docker compose -f rabbitmq.yml up -d

close-rabbitmq:
	docker compose -f rabbitmq.yml down

start-docker:
	make create-mysql
	make create-rabbitmq

close-docker:
	make close-mysql
	make close-rabbitmq

run-cerely-twse:
	pipenv run celery -A financialdata.tasks.worker worker --loglevel=info --concurrency=1 --hostname=%h -Q twse

run-everyday-twse:
	pipenv run python scheduler.py

sent-taiwan-stock-price-task:
	pipenv run python financialdata/producer.py taiwan_stock_price 20241101 20241111

gen-dev-env-var:
	python genenv.py

gen-staging-env-var:
	VERSION=STAGING python genenv.py

gen-release-env-var:
	VERSION=RELEASE python genenv.py

copy-to-service:
	sudo cp ./crawl_stock_setup.service /etc/systemd/system/
	sudo cp ./crawl_stock_run_cerely_twse.service /etc/systemd/system/
	sudo cp ./crawl_stock_run_everyday_twse.service /etc/systemd/system/
	sudo systemctl daemon-reload

enable-service:
	sudo systemctl enable crawl_stock_setup.service
	sudo systemctl enable crawl_stock_run_cerely_twse.service
	sudo systemctl enable crawl_stock_run_everyday_twse.service

start-service:
	sudo systemctl start crawl_stock_setup.service
	sudo systemctl start crawl_stock_run_cerely_twse.service
	sudo systemctl start crawl_stock_run_everyday_twse.service

close-all:
	sudo systemctl stop crawl_stock_setup.service
	sudo systemctl stop crawl_stock_run_cerely_twse.service
	sudo systemctl stop crawl_stock_run_everyday_twse.service
	make close-rabbitmq
	make close-mysql

systemctl:
	make copy-to-service
	make enable-service
	make start-service

