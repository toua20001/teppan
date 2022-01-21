import os
from logging import getLogger, config
from bs4 import BeautifulSoup as bs
from urllib import request
from typing import Union
import pandas as pd
import re
import yaml
import math
import argparse

CONFIG_FILE = "config/logging.conf"
config.fileConfig(CONFIG_FILE)
logger = getLogger(__name__)


class SearchFromNetkeiba:
    """netkeibaのデータベースページから情報を取得するためのクラス"""
    url = 'https://db.netkeiba.com/'
    pid = ""
    parameters = {}

    def __init__(self, pid: str, **kwargs):
        self.pid = pid
        self.parameters = kwargs

    def setParameters(self, k: str, v: str):
        self.parameters[k] = v

    def getSearchConditions(self) -> str:
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

    def _convParameters(self, name, value):
        if value == "":
            return ""
        else:
            return f"&{name}={value}"
    
    def getSearchResultDataFrames(self):
        cnd = self.getSearchConditions()
        url = f'{self.url}{cnd}'
        dfs = pd.read_html(url)
        return dfs

    def getSearchResultHtml(self):
        cnd = self.getSearchConditions()
        url = f'{self.url}{cnd}'
        res = request.urlopen(url)
        soup = bs(res, features="lxml")
        res.close
        return soup

    def getResultcount(self) -> Union[str, str, str]:
        html = self.getSearchResultHtml()
        pager = html.find_all(class_='pager')[0].text.replace('\n', '')
        match = re.match('(?P<count>[0-9,]*)件中(?P<start>[0-9]*)〜(?P<end>[0-9])*件目.*', pager)
        count = int(match.group('count').replace(',', ''))
        start = int(match.group('start'))
        end = int(match.group('start'))
        return count, start, end

class RaceSearch(SearchFromNetkeiba):
    """過去レースを検索するクラス"""

    def __init__(self, infilename):
        with open(infilename) as f:
            conf = yaml.safe_load(f)
        parameters = conf.get('parameters')
        self.output = conf.get('result')
        super().__init__(pid='race_list', **parameters)

    def getSearchResultDataFrames(self):
        # 検索結果の件数を取得する
        record_by_page = self.parameters.get('list', 20)
        cmax, _, _ = self.getResultcount()
        max_page = math.ceil(cmax/record_by_page)
        result = pd.DataFrame()
        logger.info('search parameters: %s', self.parameters)
        logger.info('access to: %s', self.url + self.getSearchConditions())
        logger.info('get %s records', cmax)
        # 最後のページまでデータを取得する
        for page, itr in enumerate(range(0, cmax, record_by_page), 1):
            itr_max = min(cmax, itr+record_by_page-1)
            logger.info('[%s / %s] get %s - %s records ...', page, max_page, itr, itr_max)
            self.parameters['page'] = page
            rst = super().getSearchResultDataFrames()
            result = result.append(rst[0])
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
        rs = RaceSearch(args.filename)
        rs.getSearchResultDataFrames()
        rs.save()
    elif args.mode == 'horse':
        logger.info('未実装')
        pass
    else:
        logger.warning('unknown mode: %s', args.mode)
    
    logger.info('complete.')