PROJECT_DIR := `dirname $(abspath $(MAKEFILE_LIST))`
HEADLESS := $(if $(CI), --headless, )

install:
	python3 -m pip install -U pip && \
	pip3 install -r requirements.txt

build: # this runs it in the background and can be accessed with command "docker exec -it <CONTAINER_NAME> /bin/bash"
	docker-compose up --detach

test-u:
	pytest -m unit

test-i:
	pytest -m integration

test-f:
	pytest $(HEADLESS) -m functional

test: test-u test-i test-f