from logging import getLogger
from bs4 import BeautifulSoup as bs
from urllib import request
from typing import Optional
import time
import pandas as pd
from udexception import ReadHtmlException
import configparser

# logger
logger = getLogger(__name__)
# config
config = configparser.ConfigParser()
config.read("config/teppan.conf", encoding="utf-8")


class HttpBase:
    """HPにアクセスするためのベースクラス"""
    parameters = {}
    url = None
    waittime = int(config.get("httpaccess", "waittime"))
    
    def __init__(self, url: Optional[str] = None, **kwargs):
        self.url = url
        self.parameters = kwargs

    def getHtml(self, url: Optional[str] = None):
        """対象のURLにアクセスしてHtmlデータを取得します。"""
        # urlが設定されていない場合は終了する
        if self.url is None and url is None:
            logger.error("url is not defined")
            return
        target = self.url
        if url is not None:
            target = url
        # 対象のURLにアクセスする
        ## アクセスしすぎないように１秒まつ
        time.sleep(self.waittime)
        res = request.urlopen(target)
        soup = bs(res, features="lxml")
        res.close
        return soup
        
    def setParameters(self, k: str, v: str):
        """パラメータを追加で設定する"""
        self.parameters[k] = v

    def _convParameters(self, name: str, value: str):
        """dictを検索条件形式に変形"""
        if value == "":
            return ""
        else:
            return f"&{name}={value}"

    def html_to_dataframe(self, url: str) -> pd.DataFrame:
        """pandas.DataFrame#read_htmlを使ってhtmlからテーブルのリストを取得します。"""
        try:
            return pd.read_html(url)
        except:
            logger.error(f"cannnot read html: {url}")
            raise ReadHtmlException("cannot read html: %s", url)

