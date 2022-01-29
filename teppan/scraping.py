from logging import config, getLogger
import traceback
import click
import pandas as pd
from udexception import ReadHtmlException

# logger
CONFIG_FILE = "config/logging.conf"
config.fileConfig(CONFIG_FILE)
logger = getLogger(__name__)

from racelistsearch import RaceListSearch
from racesearch import RaceSearch

@click.group()
def cli():
    pass

@cli.command()
@click.argument("configfile", type=str)
@click.argument("outfilename", type=str)
def racelist(configfile, outfilename):
        logger.info("START race list search")
        rls = RaceListSearch(configfile)
        rls.getSearchResultDataFrames()
        rls.save(outfilename)
        rls.clear()
        logger.info("complete.")

@cli.command()
@click.argument("racelist", type=str)
@click.argument("outfilename", type=str)
def races(racelist, outfilename):
    logger.info("START race detail search")
    races = pd.read_csv(racelist)
    for idx, row in races.iterrows():
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
