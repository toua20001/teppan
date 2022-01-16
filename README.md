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
```
docker-compose up
```

## モデル学習
```
docker-compose up
```

## 開発向け
```bash
# 環境の準備
## linux, macOS
python -m venv .venv

## windows（コマンドプロンプトの場合）
.venv\Scripts\activate.bat

## windows（powershellの場合）
### スクリプトの実行を許可する（１回だけ実行すれば２回目以降は不要）
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
### 仮想環境の有効化
.venv\Scripts\activate.ps1

# 共通
pip install -r requirements.txt

## 各ツールの実行
# scraping
python scrap.py

# training
python train.py

# predictiong
python predict.py

```

# Usage


# Note
