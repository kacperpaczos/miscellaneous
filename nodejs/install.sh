#!/bin/bash

# Pobieranie i instalacja NVM
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

# Ustawienie zmiennej środowiskowej NVM_DIR
export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"

# Ładowanie NVM jeśli istnieje
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

# Instalacja i użycie Node.js w wersji 18
nvm install 18
nvm use 18

# Instalacja Yarn globalnie
npm install --global yarn
