from ctypes.wintypes import HMODULE
from logging import getLogger
import os
import pandas as pd
import tempfile
import re

from httpbase import HttpBase

# logger
logger = getLogger(__name__)


class RaceSearch(HttpBase):
    """レース結果から情報を取得するクラス"""
    raceid = None
    racename = None
    baseurl = "https://db.netkeiba.com/race/{}/"

    def __init__(self, raceid: str, racename: str, **kwargs):
        self.raceid = raceid
        self.racename = racename
        url = self.baseurl.format(raceid)
        super().__init__(url, **kwargs)

    def saveas(self, outfname: str, overwrite: bool = True) -> None:
        """レース結果情報を取得してファイルに保存します。
        overwriteがTrueの場合、指定のファイル名が既に存在していれば末尾の行から追記して保存します。
        """
        # ファイル書き込みモードの設定
        mode = 'a'
        if not overwrite:
            mode = 'x'
        # レース結果の取得
        with tempfile.NamedTemporaryFile(
            mode='w+t', encoding='utf-8', delete=False, dir='./') as tfname:
            soup = self.getHtml()
            tfname.write(str(soup))
            tfname.flush()
            result = pd.read_html(tfname.name)[0]
            # 競走馬IDの一覧を取得する
            ptn = re.compile("/horse/(?P<horseid>[0-9]{10})/")
            links = soup.find("table").find_all("a")
            horseids = []
            for link in links:
                href = link.get("href")
                match = ptn.match(href)
                if match is None:
                    # 競走馬IDと一致しないリンクはスキップ
                    continue
                horseids.append(match.group("horseid"))
            result['horseid'] = horseids
            result['レース名'] = f"{self.raceid}_{self.racename}"
            # 出力ファイルに書きこむ
            # 新規作成ならヘッダーを書き込む
            header = False if os.path.exists(outfname) else True
            result.to_csv(outfname, index=False, header=header, mode=mode)



if __name__ == '__main__':
    rs = RaceSearch("202106050811", "有馬記念(G1)")
    print(rs.__dict__)
    rs.saveas("test")
