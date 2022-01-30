# teppan

[netkeiba](https://www.netkeiba.com/)から過去のレース情報を収集し、
対象レースの競走馬を相互に比較することでレースの予想をするためのツールです。

# Features
特徴があれば書く

# Requirements
- python => 3.x
- pytorch
    - [ここ](https://pytorch.org/get-started/locally/)のページを参考に環境にあったpytorchをインストールしておくこと。
- Docker
- cuda (GPU 環境を利用する場合)



# Installation

## 学習済みモデルを使用して予測
```bash
docker-compose up
```

## モデル学習
```bash
docker-compose up
```

## 開発向け
```bash
# リポジトリのclone
git clone https://github.com/toua20001/teppan.git
cd teppan

# 環境の準備
## python仮想環境の準備
python -m venv .venv

## 仮想環境の有効化
### linux, macOS
source .venv/bin/activate

### windows（コマンドプロンプトの場合）
.venv\Scripts\activate.bat

### windows（powershellの場合）
#### スクリプトの実行を許可する（１回だけ実行すれば２回目以降は不要）
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
#### 仮想環境の有効化
.venv\Scripts\activate.ps1

# 共通
pip install -r requirements.txt

# 実行する
cd teppan
python cli.py train
```

# Usage
## 過去レース、競走馬の検索

```bash
# レース一覧のデータ収集
python scraping.py racelist [検索条件の設定ファイル] [出力ファイル名]

# レースのデータ収集
# レース一覧ファイルはracelistコマンドで生成したものと同じフォーマット
python scraping.py races [レース一覧ファイル] [出力ファイル名]

# 競走馬のデータ収集
# ----- 未実装 -----
python scraping.py horse [検索条件の設定ファイル]
```

検索条件に設定できる値は[wiki参照](https://github.com/toua20001/teppan/wiki/Netkeiba%E3%81%AE%E6%A4%9C%E7%B4%A2%E6%9D%A1%E4%BB%B6)。  
結果の出力ファイルについても設定ファイル内で記載する。

```yaml
parameters:
  track[]:         # 複数選択可能な項目はリスト形式で記載する
  - 1              # 芝
  - 2              # ダート
  start_year: 2021 # 複数選択できないものは辞書形式で記載する
result:
  output: result.test.csv # 出力ファイル名の指定
```

### 例: 試しに2021年の芝のG1レースの結果を集計する
```bash
python scraping.py racelist config/2021_shiba_g1.yaml
cat result/RaceListSearch/2021_shiba_g1.csv
python scraping.py races result/RaceListSearch/2021_shiba_g1.csv
cat result/RaceSearch/2021_shiba_g1.csv
```

## 予測モデルの学習
**!! 未実装 !!**

## 学習済みモデルを使って予測
**!! 未実装 !!**

# Note
