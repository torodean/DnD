#!/bin/bash

script_dir=$(pwd)
stockpile_dir=${script_dir}/../../campaign/notes/stockpile

# Ensure we have the latest changes.
echo "Updating git repo and files to latest!"
cd ~/git/DnD/templates/stockpile
git pull

# Run the stockpile updates.
echo "Running the stockpile update!"
./stockpile.py -g ${script_dir}/stockpile_master_general.txt -t ${script_dir}/stockpile_master_trade.txt -o ${script_dir}/stockpile_inventory_lists.input -b ${script_dir}/stockpile_buy_history.txt -s ${script_dir}/stockpile_sell_history.txt

# Update the plots.
echo "Running the stockpile plot generation!"
./stockpile_plot.py -b ${script_dir}/stockpile_buy_history.txt -s ${script_dir}/stockpile_sell_history.txt -o ${stockpile_dir}/plots

# Update the HTML page.
echo "Updating the stockpile HTML pages!"
cd ..
./creator.py -f ${script_dir}/stockpile_inventory_lists.input

# Add the new updated files to the git repo.
echo "Updating the git repo with the new files!"
git add -A
git commit -m "Automatic stockpile update."
git push origin main

# Update the public MMORPDND database to reflect changes.
echo "Updating the MMORPDND git database with the new files!"
cd ~/git/MMORPDND.github.io/
git pull
./updateSubmodules.sh
git add -A
git commit -m "Automatic database update for stockpile updates"
git push origin main
