#!/bin/bash

# directory where this script exists
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR
echo $DIR
cd ../..
echo $(pwd)
python -m masakari.engine.db.create_tables
