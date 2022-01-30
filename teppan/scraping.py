import os
from logging import config, getLogger
import traceback
import click
import pandas as pd
from udexception import ReadHtmlException
import configparser

# logger
CONFIG_FILE = "config/logging.conf"
config.fileConfig(CONFIG_FILE)
logger = getLogger(__name__)

from racelistsearch import RaceListSearch
from racesearch import RaceSearch

# config
config = configparser.ConfigParser()
config.read("config/teppan.conf", encoding="utf-8")


def getOutputFilename(optname: str, inputfilename: str, ext: str) -> str:
    """入力ファイル名から出力ファイルパスを作る"""
    outdir = config.get(optname, "outdir")
    if not os.path.exists(outdir):
        logger.info(f"create output dir: {outdir}")
        os.makedirs(outdir)
    fname = os.path.splitext(os.path.basename(inputfilename))[0]
    outfilename = os.path.join(outdir, fname + ext)
    return outfilename


@click.group()
def cli():
    pass


@cli.command()
@click.argument("configfile", type=str)
def racelist(configfile):
        logger.info("START race list search")
        outfilename = getOutputFilename("RaceListSearch", configfile, ".csv")
        rls = RaceListSearch(configfile)
        rls.getSearchResultDataFrames()
        rls.save(outfilename)
        rls.clear()
        logger.info("complete.")


@cli.command()
@click.argument("racelist", type=str)
def races(racelist):
    logger.info("START race detail search")
    outfilename = getOutputFilename("RaceSearch", racelist, ".csv")
    races = pd.read_csv(racelist)
    size = len(races)
    for idx, row in races.iterrows():
        raceid = row['raceid']
        racename = row['レース名']
        logger.info(f"search target ({idx+1}/{size}): ID={raceid}, name={racename}")
        try:
            rs = RaceSearch(row['raceid'], row['レース名'])
            rs.saveas(outfilename)
        except ReadHtmlException:
            logger.warning(f"skiped: ID={row['raceid']}, name={row['レース名']}")
    logger.info("complete.")


if __name__ == '__main__':
    try:
        cli()
    except Exception:
        traceback.print_exc()
        logger.info("Abort.")
