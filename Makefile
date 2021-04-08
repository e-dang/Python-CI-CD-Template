PROJECT_DIR := `dirname $(abspath $(MAKEFILE_LIST))`
HEADLESS := $(if $(CI), --headless, )

install:
	python3 -m pip install -U pip && \
	pip3 install -r requirements.txt && \
	pip3 install -r test-requirements.txt

build: # this runs it in the background and can be accessed with command "docker exec -it <CONTAINER_NAME> /bin/bash"
	docker-compose up --detach

test-u:
	pytest -m unit

test-i:
	pytest -m integration

test-f:
	echo "Testing against local test server..." && \
	pytest $(HEADLESS) -m functional

test-f-docker: build
	echo "Testing against docker container..." && \
	SERVER_URL=http://localhost:8000 pytest $(HEADLESS) -m functional

test: test-u test-i test-f