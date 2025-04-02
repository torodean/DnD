#!/usr/bin/env python3

# This is a test script for plotting all HTML files as nodes and connecting them via their links.

import os
import networkx as nx
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import plotly.graph_objects as go


def extract_links(html_content):
    """
    Extracts and returns all links to HTML files from the provided HTML content.
    
    Args:
        html_content (str): HTML content as a string.
        
    Returns:
        list: A list of extracted links that point to HTML files.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    return [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.html')]

def build_graph(directory):
    """
    Builds a directed graph from HTML files found in the given directory and its subdirectories.
    Each node represents an HTML file, and each directed edge represents a link from one HTML file to another.
    
    Args:
        directory (str): The path to the directory containing HTML files.
        
    Returns:
        networkx.DiGraph: A directed graph representing the links between HTML files.
    """
    G = nx.DiGraph()

    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.html') and filename != 'index.html' and "_public" not in filename:
                filepath = os.path.join(root, filename)
                filename = filename.split(".htm")[0]
                G.add_node(filename)  # Add the node for the HTML file
                
                with open(filepath, 'r', encoding='utf-8') as file:
                    html_content = file.read()
                    links = extract_links(html_content)
                    for link in links:
                        # Ensure the link is relative and points to another HTML file within the directory
                        if link.endswith('.html') and 'index.html' not in link:
                            linked_file = os.path.join(root, link)
                            if os.path.isfile(linked_file):
                                link = link.replace("../", "")
                                link = link.split("/")[-1].split(".htm")[0]
                                G.add_edge(filename, link)
                        
    return G


def visualize_graph_plotly(G):
    """
    Visualizes the directed graph G using Plotly for interactive plotting.
    
    Nodes represent HTML files, and edges represent links between HTML files.
    
    Args:
        G (networkx.DiGraph): A directed graph to visualize.
        
    Returns:
        None: Displays an interactive Plotly graph.
    """
    pos = nx.spring_layout(G, k=0.5, iterations=50)  # Adjust the 'k' and 'iterations' parameters

    edge_x = []
    edge_y = []

    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    node_text = []
    node_size = []

    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)
        node_size.append(8 + 1.05 * G.degree(node))  # Adjust node size based on degree

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=node_text,
        textposition="top center",
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            size=node_size,  # Set the node size dynamically
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='Network graph of HTML links',
                        titlefont_size=16,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        xaxis=dict(showgrid=False, zeroline=False),
                        yaxis=dict(showgrid=False, zeroline=False))
                    )
    fig.show()

directory = '../campaign'
G = build_graph(directory)
visualize_graph_plotly(G)
