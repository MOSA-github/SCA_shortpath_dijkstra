# SCA_shortpath_dijkstra

Safety Charging Area (SCA) への最短経路をダイクストラ法で計算するプロジェクトです。

---

## 1. ダイクストラ法とは

**ダイクストラ法（Dijkstra's Algorithm）** は、重み付きグラフにおいて、ある始点から他のすべてのノードへの最短経路を求めるアルゴリズムです。

### アルゴリズムの流れ

1. **初期化**
   - 始点ノードの距離を `0`、他のすべてのノードの距離を `∞`（無限大）に設定
   - すべてのノードを「未確定」としてマーク

2. **最小距離ノードの選択**
   - 未確定ノードの中から、始点からの距離が最小のノードを選択

3. **隣接ノードの距離更新**
   - 選択したノードの隣接ノードに対して、現在の経路より短い経路があれば距離を更新
   - 更新式: `新しい距離 = 現在のノードまでの距離 + エッジの重み`

4. **ノードを確定**
   - 選択したノードを「確定」としてマーク

5. **繰り返し**
   - すべてのノードが確定するまで、手順2〜4を繰り返す

### 計算量

- **時間計算量**: O((V + E) log V)（優先度付きキュー使用時）
  - V: ノード数、E: エッジ数

### 特徴

- **非負の重み**を持つグラフでのみ正しく動作
- 貪欲法（Greedy Algorithm）に基づく
- 最短経路木を構築可能

---

## 2. ファイル構成

```
SCARootMOSA/
├── SCA_dijkstra.py          # メインプログラム（ダイクストラ法による最短経路計算）
├── shortest_paths.yaml      # 計算結果（各ノードからSCAへの経路情報）
├── graph_visualization.png  # グラフの可視化画像
├── requirements.txt         # 必要なPythonパッケージ一覧
├── README.md                # このファイル
├── .gitignore               # Git除外設定
└── SCAenv/                  # Python仮想環境（.gitignoreで除外）
```

### 各ファイルの説明

| ファイル名 | 説明 |
|-----------|------|
| `SCA_dijkstra.py` | ダイクストラ法を用いて最短経路を探索するメインコード。NetworkXを使用してグラフを構築し、各ノードからSCAへの最短経路をYAMLに保存します。 |
| `shortest_paths.yaml` | 各ノードからSCA（ノード0）への最短距離と経路情報。グラフの重み付けルールも記載。 |
| `graph_visualization.png` | 作成したグラフの可視化画像。エッジの色で重み（距離）を区別。 |
| `requirements.txt` | 必要なパッケージ（networkx, pyyaml, matplotlib）の一覧。 |

---

## 3. 使い方

### 環境構築

```bash
# 仮想環境の作成と有効化
python -m venv SCAenv
.\SCAenv\Scripts\activate  # Windows
source SCAenv/bin/activate  # Mac/Linux

# パッケージのインストール
pip install -r requirements.txt
```

### 実行

```bash
python SCA_dijkstra.py
```

### 出力

- `shortest_paths.yaml`: 最短経路の計算結果
- `graph_visualization.png`: グラフの可視化画像（GUI環境がある場合）
