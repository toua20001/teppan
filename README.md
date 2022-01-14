# teppan

[netkeiba](https://www.netkeiba.com/)から過去のレース情報を収集し、
対象レースの競走馬を相互に比較することでレースの予想をするためのツールです。

# Features
特徴があれば書く

# Requirements
- python => 3.x
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
```
# prepare enviroments
python -m venv .venv
pip install requirements.txt

# scraping
python scrap.py

# training
python train.py

# predictiong
python predict.py

```

# Usage


# Note
