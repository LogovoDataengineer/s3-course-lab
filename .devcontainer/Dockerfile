FROM mcr.microsoft.com/devcontainers/python:1-3.12-bookworm

# Yarn is not used by this course. Its stale signing key in the base image
# otherwise prevents apt from installing the Docker-in-Docker feature.
RUN rm -f /etc/apt/sources.list.d/yarn.list /etc/apt/sources.list.d/yarn.sources
