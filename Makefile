.PHONY: build deploy docker-build docker-run install test template

build:
	bash bin/build.sh

deploy:
	bash bin/deploy.sh

docker-build:
	bash bin/docker-build.sh

docker-run:
	bash bin/docker-run.sh

install:
	bash bin/install.sh

test:
	bash bin/test.sh

template:
	bash bin/preview.sh