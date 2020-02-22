import xmltodict
import json
import argparse
import torchvision
import os

from pathlib import Path
from utils.utils import Colors, METHODS, DATASET_TO_FOLDER_NAME
from utils.graph import generate_fname, get_parser, read_graph, get_roots
from networkx.readwrite.json_graph import adjacency_data


parser = get_parser()
args = parser.parse_args()

folder = DATASET_TO_FOLDER_NAME[args.dataset]
directory = os.path.join('data', folder)

fname = generate_fname(**vars(args))
path = os.path.join(directory, f'{fname}.json')
print('==> Reading from {}'.format(path))


def build_tree(root, parent='null'):
    return {
        'name': root,
        'parent': parent,
        'children': [build_tree(child, root) for child in G.succ[root]]
    }


def build_graph():
    return {
        'nodes': [{
            'name': wnid,
            'label': wnid,
            'id': wnid
        } for wnid in G.nodes],
        'links': [{
            'source': u,
            'target': v
        } for u, v in G.edges]
    }


def generate_vis(path_template, data, name):
    with open(path_template) as f:
        html = f.read().replace(
            "'TREE_DATA_CONSTANT_TO_BE_REPLACED'",
            json.dumps(data))

    os.makedirs('out', exist_ok=True)
    path_html = f'out/{fname}-{name}.html'
    with open(path_html, 'w') as f:
        f.write(html)

    Colors.green('==> Wrote HTML to {}'.format(path_html))


G = read_graph(path)
print(len(list(get_roots(G))))
root = next(get_roots(G))
tree = build_tree(root)
graph = build_graph()

generate_vis('vis/tree-template.html', tree, 'tree')
generate_vis('vis/graph-template.html', graph, 'graph')
