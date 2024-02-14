#!/bin/python3
import os
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser(description='S.T.O.C.K.P.I.L.E.S price history plotting.')

parser.add_argument('-H', '--history',
                    required=True,
                    action='store',
                    help='The file containing price history for the stockpile items.')
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

def read_data(filename):
    items = {}
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split(';')
            item_name = parts[0]
            prices = [float(price) for price in parts[1:]]
            items[item_name] = prices
    return items

def plot_price_history(item_name, item_prices, item_index=0, total_num_items=0):
    plt.plot(range(1, len(item_prices) + 1), item_prices, marker='o')
    plt.title(f'Price History of {item_name}')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.grid(True)
    if args.item == None:
        print(f"Creating plot {item_index} of {total_num_items}. Please wait...")
        filename = f"{args.output}/{item_name.replace(' ', '_')}_price_history.png"
        plt.savefig(filename)  # Save the plot to the specified filename
        plt.close()  # Close the plot to free up memory
    else:
        plt.show()

def main():
    filename = args.history
    items = read_data(filename)

    search_item = args.item

    if search_item == None:
        index = 0
        for item in items:
            plot_price_history(item, items[item], index, len(items))
            index = index + 1
    elif search_item in items:
        plot_price_history(search_item, items[search_item])
    else:
        print(f"Item '{search_item}' not found.")

if __name__ == "__main__":
    main()
