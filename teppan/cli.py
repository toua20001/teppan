#!/usr/bin/env python
import click
from logging import getLogger, config

CONFIG_FILE = "config/logging.conf"
config.fileConfig(CONFIG_FILE)
logger = getLogger()

@click.group()
def cli():
    logger.info('##### start teppan app #####')

@cli.command()
def scraping():
    logger.info('scraping scraping')

@cli.command()
def train():
    logger.info('start training')

@cli.command()
def predict():
    logger.info('start predicting')

if __name__ == '__main__':
    cli()
