import argparse
from logging import config, getLogger
import traceback

# logger
CONFIG_FILE = "config/logging.conf"
config.fileConfig(CONFIG_FILE)
logger = getLogger(__name__)

from racelistsearch import RaceListSearch


def race_list_search():
        logger.info('start scraping ...')
        rls = RaceListSearch(args.filename)
        rls.getSearchResultDataFrames()
        rls.save()
        rls.clear()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['race', 'horse'], help='検索対象（race: レース, horse: 競走馬）')
    parser.add_argument('filename', help='検索条件をの設定ファイル')
    args = parser.parse_args()

    try:
        if args.mode == 'race':
            race_list_search()
        elif args.mode == 'horse':
            logger.info('未実装')
            pass
        else:
            logger.warning('unknown mode: %s', args.mode)
    except Exception:
        traceback.print_exc()
        logger.info("エラーが発生したため終了します。")
    
    logger.info('complete.')