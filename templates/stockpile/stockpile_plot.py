#!/usr/bin/env python3
import os
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser(description='S.T.O.C.K.P.I.L.E.S price history plotting.')

parser.add_argument('-b', '--buy',
                    required=True,
                    action='store',
                    help='The file containing buy price history for the stockpile items.')
parser.add_argument('-s', '--sell',
                    required=True,
                    action='store',
                    help='The file containing sell price history for the stockpile items.')
parser.add_argument('-i', '--item',
                    action='store',
                    help='The item to search for and plot. This will display the plot as well. If not specified, all plots will be generated.')
parser.add_argument('-o', '--output',
                    action='store',
                    default='stockpile_plots',
                    help='The folder to output all plots to. This option will be ignored if \'-i\' is specified.')

args = parser.parse_args()

# Print the value of args.output for debugging
print("Output directory:", args.output)

if args.output:
    # Create directory if it doesn't exist
    if not os.path.exists(args.output):
        os.makedirs(args.output)

def read_data(filename_buy, filename_sell):
    items_buy = {}
    items_sell = {}
    with open(filename_buy, 'r') as file_buy, open(filename_sell, 'r') as file_sell:
        for line_buy, line_sell in zip(file_buy, file_sell):
            parts_buy = line_buy.strip().split(';')
            parts_sell = line_sell.strip().split(';')
            item_name_buy = parts_buy[0]
            item_name_sell = parts_sell[0]
            prices_buy = [float(price) for price in parts_buy[1:]]
            prices_sell = [float(price) for price in parts_sell[1:]]
            items_buy[item_name_buy] = prices_buy
            items_sell[item_name_sell] = prices_sell
    return items_buy, items_sell

def plot_price_history(item_name, item_prices_buy, item_prices_sell, item_index=0, total_num_items=0):
    plt.plot(range(1, len(item_prices_buy) + 1), item_prices_buy, marker='o', label='Buy Price')
    plt.plot(range(1, len(item_prices_sell) + 1), item_prices_sell, marker='o', label='Sell Price')
    plt.title(f'Price History of {item_name}')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    if args.item == None:
        print(f"Creating plot {item_index} of {total_num_items}. Please wait...")
        filename = f"{args.output}/{item_name.replace(' ', '_')}_price_history.png"
        plt.savefig(filename)  # Save the plot to the specified filename
        plt.close()  # Close the plot to free up memory
    else:
        plt.show()

def main():
    filename_buy = args.buy
    filename_sell = args.sell
    items_buy, items_sell = read_data(filename_buy, filename_sell)

    search_item = args.item

    if search_item == None:
        index = 0
        for item in items_buy:
            plot_price_history(item, items_buy[item], items_sell[item], index, len(items_buy))
            index += 1
    elif search_item in items_buy:
        plot_price_history(search_item, items_buy[search_item], items_sell[search_item])
    else:
        print(f"Item '{search_item}' not found.")

if __name__ == "__main__":
    main()
