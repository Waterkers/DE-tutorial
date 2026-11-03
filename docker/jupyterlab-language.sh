#!/bin/bash
# Container start hook (before-notebook.d): set JupyterLab's own menus to the
# language of the practical (PRACTICAL_LANG=en|de) and turn off the "Jupyter news"
# popup, which only distracts students.
settings="/home/${NB_USER}/.jupyter/lab/user-settings/@jupyterlab"
mkdir -p "${settings}/translation-extension" "${settings}/apputils-extension"
if [ "${PRACTICAL_LANG}" = "de" ]; then locale="de_DE"; else locale="en"; fi
echo "{ \"locale\": \"${locale}\" }" > "${settings}/translation-extension/plugin.jupyterlab-settings"
echo '{ "fetchNews": "false", "checkForUpdates": false }' > "${settings}/apputils-extension/notification.jupyterlab-settings"
if [ "$(id -u)" = "0" ]; then
    chown -R "${NB_UID}:${NB_GID}" "/home/${NB_USER}/.jupyter"
fi
