from logging import getLogger
from bs4 import BeautifulSoup as bs
from urllib import request
from typing import Optional
import time

# logger
logger = getLogger(__name__)


class HttpBase:
    """HPにアクセスするためのベースクラス"""
    parameters = {}
    url = None
    
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
        time.sleep(1)
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

