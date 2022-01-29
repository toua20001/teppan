import os
from logging import getLogger, config
from bs4 import BeautifulSoup as bs
from urllib import request
from typing import Optional, Union
import pandas as pd
import re
import yaml
import math
import argparse
import tempfile
import time

# logger
CONFIG_FILE = "config/logging.conf"
config.fileConfig(CONFIG_FILE)
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


class SearchFromNetkeiba(HttpBase):
    """netkeibaのデータベースページから情報を取得するためのクラス"""
    pid = ""
    localfilename = None

    def __init__(self, pid: str, **kwargs):
        self.pid = pid
        super().__init__(url='https://db.netkeiba.com/', **kwargs)

    def getSearchConditions(self) -> str:
        """検索条件をURLの形式で取得する"""
        result = f"?pid={self.pid}"
        for k, v in self.parameters.items():
            if isinstance(v, list):
            # 複数選択可能なパラメータの場合、同じ属性値を繰り返して指定
                for v1 in v:
                    result+= self._convParameters(k, v1)
            else:
            # １つのみ指定の場合はそのまま属性値に設定
                result += self._convParameters(k, v)
        return result

    def getSearchResultDataFrames(self) -> pd.DataFrame:
        """DataFrame形式で検索結果を取得する"""
        cnd = self.getSearchConditions()
        if self.localfilename is None:
            # HPにアクセスする
            url = f'{self.url}{cnd}'
            logger.info(f"GET {url}")
            dfs = pd.read_html(url)
        else:
            # ローカルにファイルが保存してあればそのファイルを読み込む
            logger.info(f"load localfile: {self.localfilename}")
            dfs = pd.read_html(self.localfilename)
        return dfs

    def getSearchResultHtml(self, savefile: bool = True) -> bs:
        """html形式で結果を取得する"""
        cnd = self.getSearchConditions()
        url = f'{self.url}{cnd}'
        logger.info(f"GET {url}")
        soup = self.getHtml(url)
        if savefile:
            # 一時ファイルに書き出す
            if self.localfilename is None:
                with tempfile.NamedTemporaryFile(
                    mode='w+t', encoding='utf-8', delete=False, dir='./') as tfname:
                    tfname.write(str(soup))
                    self.localfilename = tfname.name
                    logger.info(f"http response save as {self.localfilename}")
            else:
                with open(self.localfilename, 'w+t', encoding='utf-8') as tfname:
                    tfname.write(str(soup))
                    logger.info(f"http response save as {self.localfilename}")
        return soup

    def getResultcount(self) -> Union[str, str, str]:
        """検索結果の件数を取得する"""
        try:
            html = self.getSearchResultHtml()
            pager = html.find(class_='pager').text
            pager = pager.replace('\n', '')
            match = re.search('(?P<count>[0-9,]+)件中(?P<start>[0-9]+).*(?P<end>[0-9]+)件目', pager)
            count = int(match.group('count').replace(',', ''))
            start = int(match.group('start'))
            end = int(match.group('start'))
        except:
            count = 0
            start = 0
            end = 0
        return count, start, end

    def clear(self):
        if os.path.exists(self.localfilename):
            logger.info(f"remove localfile: {self.localfilename}")
            os.remove(self.localfilename)

class RaceListSearch(SearchFromNetkeiba):
    """過去レースを検索するクラス"""

    def __init__(self, infilename):
        with open(infilename) as f:
            conf = yaml.safe_load(f)
        parameters = conf.get('parameters')
        self.output = conf.get('result')
        super().__init__(pid='race_list', **parameters)

    def _get_race_ids(self):
        """検索結果のhtmlからレースIDのリストを取得する"""
        ptn = re.compile("/race/(?P<raceid>[0-9a-zA-z]{12})/")  # レースIDのパターン
        soup = self.getSearchResultHtml()
        raceids = []
        for links in soup.find('table').find_all('a'):
            href = links.get('href')
            match = ptn.match(href)
            if match is None:
                continue  # レース以外のリンクはスキップする
            # リンクのID部分だけを抽出する
            raceids.append(match.group("raceid"))
        return raceids

    def getSearchResultDataFrames(self):
        # 検索結果の件数を取得する
        record_by_page = self.parameters.get('list', 20)
        cmax, _, _ = self.getResultcount()
        max_page = math.ceil(cmax/record_by_page)
        result = None
        logger.info('search parameters: %s', self.parameters)
        logger.info('access to: %s', self.url + self.getSearchConditions())
        logger.info('get %s records', cmax)
        cmax = 1 if cmax == 0 else cmax  # cmaxが0でも1回はデータ取得を試みる
        # 最後のページまでデータを取得する
        for page, itr in enumerate(range(0, cmax, record_by_page), 1):
            # このイテレーションで取得するテーブルサイズ
            itr_max = min(cmax, itr+record_by_page-1)
            logger.info('[%s / %s] get %s - %s records ...', page, max_page, itr, itr_max)
            # ページを指定して検索
            self.parameters['page'] = page
            # レースのリンクを取得する
            raceids = self._get_race_ids()
            # 検索結果の取得
            gsrdf = super().getSearchResultDataFrames()[0]
            # レースリンク情報を追加
            gsrdf['raceid'] = raceids
            # 結果のタンキング
            if result is None:
                result = gsrdf
            else:
                result = pd.concat([result, gsrdf], axis=0)
        self.result = result
        return self.result

    def save(self, outfname=None):
        if outfname is None:
            outfname = self.output.get('output')
        dname = os.path.dirname(outfname)
        os.makedirs(dname, exist_ok=True)
        self.result.to_csv(outfname)
        logger.info('output result data: %s', outfname)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['race', 'horse'], help='検索対象（race: レース, horse: 競走馬）')
    parser.add_argument('filename', help='検索条件をの設定ファイル')
    args = parser.parse_args()

    if args.mode == 'race':
        logger.info('start scraping ...')
        rls = RaceListSearch(args.filename)
        rls.getSearchResultDataFrames()
        rls.save()
        rls.clear()
    elif args.mode == 'horse':
        logger.info('未実装')
        pass
    else:
        logger.warning('unknown mode: %s', args.mode)
    
    logger.info('complete.')