FROM debian:bullseye-slim

RUN apt-get update && \
	export DEBIAN_FRONTEND=noninteractive && \
	apt-get install --yes --no-install-recommends build-essential debhelper dh-python python3-all python3-setuptools python3-django python3-django-macaddress python3-click python3-qrcode python3-pytest python3-pytest-django python3-pytest-cov