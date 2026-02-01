"""
格子状グラフの作成とダイクストラ法による最短経路計算
- ノード0（Safety Charging Area）から各ノードへの最短経路を計算
- 結果をYAMLファイルに保存
"""

import networkx as nx
import yaml
import matplotlib.pyplot as plt


def create_grid_graph():
    """
    画像に基づいて格子状グラフを作成

    ノード配置（グリッド座標）:
        行0: 7  6  -  5  4
        行1: 8  11 -  2  3
        行2: 9  10 -  1  0(Safety)

    「-」はソーラーパネル領域（ノードなし）

    距離の重み付け:
        - 長い（ソーラーパネルをまたぐ横方向）: 2
        - 中間（通常の縦方向）: 1
        - 短い（短い横方向）: 0.5
    """
    G = nx.Graph()

    # ノードを追加（0-11）
    # 座標情報も追加（可視化用）
    node_positions = {
        0: (4, 0),   # Safety Charging Area (右下)
        1: (3, 0),
        2: (3, 1),
        3: (4, 1),
        4: (4, 2),
        5: (3, 2),
        6: (1, 2),
        7: (0, 2),
        8: (0, 1),
        9: (0, 0),
        10: (1, 0),
        11: (1, 1),
    }

    for node, pos in node_positions.items():
        G.add_node(node, pos=pos)

    # エッジを追加（重み付き）
    # 重み: 長い=2, 中間=1, 短い=0.5

    edges_with_weights = [
        # 右側の列（0-1-2-3-4-5）の縦方向接続
        (0, 1, 0.5),   # 短い横方向
        (0, 3, 1),     # 縦方向
        (1, 2, 1),     # 縦方向
        (2, 3, 0.5),   # 短い横方向
        (2, 5, 1),     # 縦方向
        (3, 4, 1),     # 縦方向
        (4, 5, 0.5),   # 短い横方向

        # 左側の列（7-8-9, 6-11-10）の接続
        (7, 6, 2),   # 長い横方向
        (7, 8, 1),     # 縦方向
        (6, 11, 1),    # 縦方向
        (8, 9, 1),     # 縦方向
        (8, 11, 2),  # 長い横方向
        (9, 10, 2),  # 長い横方向
        (10, 11, 1),   # 縦方向

        # ソーラーパネルをまたぐ横方向接続（長い距離=2）
        (5, 6, 2),     # 上段：5-6（ソーラーパネルをまたぐ）
        (2, 11, 2),    # 中段：2-11（ソーラーパネルをまたぐ）
        (1, 10, 2),    # 下段：1-10（ソーラーパネルをまたぐ）
    ]

    for node1, node2, weight in edges_with_weights:
        G.add_edge(node1, node2, weight=weight)

    return G, node_positions


def compute_shortest_paths(G, target_node=0):
    """
    ダイクストラ法で各ノードからtarget_nodeへの最短経路を計算

    Args:
        G: NetworkXグラフ
        target_node: 目的地ノード（デフォルトは0=Safety Charging Area）

    Returns:
        dict: 各始点ノードからの経路情報
    """
    paths_info = {}

    for source_node in G.nodes():
        if source_node == target_node:
            continue

        try:
            # ダイクストラ法で最短経路を計算
            path = nx.dijkstra_path(G, source_node, target_node, weight='weight')
            path_length = nx.dijkstra_path_length(G, source_node, target_node, weight='weight')

            paths_info[source_node] = {
                'start': source_node,
                'goal': target_node,
                'path': path,
                'total_weight': float(path_length),
                'path_description': ' -> '.join(map(str, path))
            }
        except nx.NetworkXNoPath:
            paths_info[source_node] = {
                'start': source_node,
                'goal': target_node,
                'path': None,
                'total_weight': float('inf'),
                'path_description': 'No path found'
            }

    return paths_info


def save_to_yaml(paths_info, filename='shortest_paths.yaml'):
    """
    経路情報をYAMLファイルに保存

    Args:
        paths_info: 経路情報の辞書
        filename: 出力ファイル名
    """
    # YAMLに保存しやすい形式に変換
    yaml_data = {
        'graph_info': {
            'description': 'Grid graph with Safety Charging Area as node 0',
            'weight_rules': {
                'long_distance': 2.0,
                'medium_distance': 1.0,
                'short_distance': 0.5
            }
        },
        'shortest_paths': {}
    }

    for node, info in sorted(paths_info.items()):
        yaml_data['shortest_paths'][f'from_node_{node}'] = {
            'start_node': info['start'],
            'goal_node': info['goal'],
            'route': info['path'],
            'total_distance': info['total_weight'],
            'description': info['path_description']
        }

    with open(filename, 'w', encoding='utf-8') as f:
        yaml.dump(yaml_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    print(f"経路情報を '{filename}' に保存しました。")


def visualize_graph(G, node_positions, paths_info=None):
    """
    グラフを可視化

    Args:
        G: NetworkXグラフ
        node_positions: ノードの座標辞書
        paths_info: 経路情報（オプション）
    """
    plt.figure(figsize=(12, 8))

    # ノードの描画
    nx.draw_networkx_nodes(G, node_positions, node_color='lightblue',
                        node_size=700, alpha=0.9
                        )

    # ノード0（Safety Charging Area）を特別な色で表示
    nx.draw_networkx_nodes(G, node_positions, nodelist=[0],
                        node_color='lightgreen', node_size=900, alpha=0.9
                        )

    # エッジの描画（重みによって色分け）
    edge_colors = []
    edge_widths = []
    for u, v, data in G.edges(data=True):
        weight = data['weight']
        if weight == 2:
            edge_colors.append('red')
            edge_widths.append(2)
        elif weight == 1:
            edge_colors.append('orange')
            edge_widths.append(1.5)
        else:
            edge_colors.append('green')
            edge_widths.append(1)

    nx.draw_networkx_edges(G, node_positions, edge_color=edge_colors,
                        width=edge_widths, alpha=0.7
                        )

    # エッジの重みをラベルとして表示
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, node_positions, edge_labels=edge_labels,
                                font_size=8
                                )

    # ノードラベルの描画
    labels = {0: '0\n(Safety)'}
    for i in range(1, 12):
        labels[i] = str(i)
    nx.draw_networkx_labels(G, node_positions, labels, font_size=10, font_weight='bold')

    plt.title('Grid Graph with Weighted Edges\n(Green=0.5, Orange=1, Red=2)')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('graph_visualization.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("グラフを 'graph_visualization.png' に保存しました。")


def main():
    print("=" * 60)
    print("格子状グラフの作成と最短経路計算")
    print("=" * 60)

    # グラフ作成
    print("\n[1] グラフを作成中...")
    G, node_positions = create_grid_graph()
    print(f"    ノード数: {G.number_of_nodes()}")
    print(f"    エッジ数: {G.number_of_edges()}")

    # グラフ構造の表示
    print("\n[2] グラフ構造:")
    print("    エッジ一覧（ノード1 -- ノード2 : 重み）:")
    for u, v, data in sorted(G.edges(data=True)):
        print(f"      {u:2d} -- {v:2d} : {data['weight']}")

    # ダイクストラ法で最短経路を計算
    print("\n[3] ダイクストラ法で最短経路を計算中...")
    paths_info = compute_shortest_paths(G, target_node=0)

    # 結果の表示
    print("\n[4] 計算結果:")
    for node in sorted(paths_info.keys()):
        info = paths_info[node]
        print(f"    ノード{node} -> ノード0: {info['path_description']} (距離: {info['total_weight']})")

    # YAMLファイルに保存
    print("\n[5] 結果をYAMLファイルに保存中...")
    save_to_yaml(paths_info, 'shortest_paths.yaml')

    # グラフの可視化
    print("\n[6] グラフを可視化中...")
    try:
        visualize_graph(G, node_positions, paths_info)
    except Exception as e:
        print(f"    可視化でエラーが発生しました: {e}")
        print("    （matplotlibのGUI環境がない場合があります）")

    print("\n" + "=" * 60)
    print("完了!")
    print("=" * 60)


if __name__ == '__main__':
    main()
