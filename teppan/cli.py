#!/usr/bin/env python
import click


@click.group()
def cli():
    pass

@cli.command()
def scraping():
    pass

@cli.command()
def training():
    pass

@cli.command()
def predict():
    pass

if __name__ == '__main__':
    cli()
