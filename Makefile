.PHONY: docker_prepare _docker_prepare

docker_prepare:
	docker exec -it $(shell docker ps -q -f name=datapicker_data-picker_1) /bin/bash -c "python manage.py migrate"
	docker exec -it $(shell docker ps -q -f name=datapicker_data-picker_1) /bin/bash -c "python manage.py createsuperuserauto"
