#!/bin/bash

# https://docs.npmjs.com/cli/cache
npm cache verify

# install project dependencies
npm install
echo "testtttttttttttttttttttttttttttttttttttt"
# run the development server
npm run serve