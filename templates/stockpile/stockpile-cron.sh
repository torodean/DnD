#!/bin/bash

#TODO - This is just a mock script. Paths and things need finalized.

# Ensure we have the latest changes.
cd ~/DnD/templates/stockpile
git pull

# Run the stockpile updates.
./stockpile.py -g stockpile_master_general.txt -t stockpile_master_trade.txt -o stockpile_inventory_lists.input -b stockpile_buy_history.txt -s stockpile_sell_history.txt

# Update the plots.
./stockpile_plot.py -b stockpile_buy_history.txt -s stockpile_sell_history.txt -o plots

# Update the HTML page.
#TODO - finish adding -f capabilities to creator.py
../creator.py -f stockpile/

git add -A
git commit -m "Automatic stockpile update."
git push origin main

# Update the public MMORPDND database to reflect changes
# TODO
cd ~/MMORPDND.github.io/
git pull
./updateSubmodules.sh
git add -A
git commit -m "Automatic database update for stockpile updates"
git push origin main
