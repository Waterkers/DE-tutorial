#!/bin/bash
# Container start hook (before-notebook.d), runs as root before Jupyter starts.
# start.sh gives the notebook user the host's user ID, so notebooks students save
# belong to them. The image's own start script then re-owns only the home folder
# itself, not what's inside it (.local, .cache, .jupyter still belong to the
# image's user 1000), and Jupyter fails with "Permission denied". Re-own the
# contents too, except the mounted practical/ folder: those are the host's files.
if [ "$(id -u)" = "0" ]; then
    find "/home/${NB_USER}" -mindepth 1 -maxdepth 1 ! -name practical \
        -exec chown -R "${NB_UID}:${NB_GID}" {} +
fi
