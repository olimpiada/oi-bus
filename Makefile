CONTAINER_NAME = dev

define run_in_docker
	docker build -t oi-bus-dev .
	- docker run --rm --volume $(shell pwd):/app/oi-bus --workdir /app/oi-bus --name $(CONTAINER_NAME) -d -it oi-bus-dev
	docker exec $(CONTAINER_NAME) $(1)
	docker stop $(CONTAINER_NAME)
endef


build-docker:
	$(call run_in_docker,make build)

build:
	dpkg-buildpackage -uc -us
	mkdir -p out
	mv ../*.deb out/

clean-docker: 
	$(call run_in_docker,make clean)

clean:
	- rm -rf out