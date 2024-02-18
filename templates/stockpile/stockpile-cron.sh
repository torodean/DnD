#!/bin/bash

script_dir=$(pwd)
stockpile_dir=${script_dir}/../../campaign/notes/stockpile

# Ensure we have the latest changes.
cd ~/DnD/templates/stockpile
git pull

# Run the stockpile updates.
./stockpile.py -g ${script_dir}/stockpile_master_general.txt -t ${script_dir}/stockpile_master_trade.txt -o ${script_dir}/stockpile_inventory_lists.input -b ${script_dir}/stockpile_buy_history.txt -s ${script_dir}/stockpile_sell_history.txt

# Update the plots.
./stockpile_plot.py -b ${script_dir}/stockpile_buy_history.txt -s ${script_dir}/stockpile_sell_history.txt -o ${stockpile_dir}/plots

# Update the HTML page.
../creator.py -f ${script_dir}/stockpile_inventory_lists.input

git add -A
git commit -m "Automatic stockpile update."
git push origin main

# Update the public MMORPDND database to reflect changes
cd ~/MMORPDND.github.io/
git pull
./updateSubmodules.sh
git add -A
git commit -m "Automatic database update for stockpile updates"
git push origin main
