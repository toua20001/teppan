import argparse
from logging import config, getLogger

# logger
CONFIG_FILE = "config/logging.conf"
config.fileConfig(CONFIG_FILE)
logger = getLogger(__name__)

from racelistsearch import RaceListSearch


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