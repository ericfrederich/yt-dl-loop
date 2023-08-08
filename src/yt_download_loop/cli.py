import click


@click.command()
def cli_main():
    click.secho("HI", fg="green", bold=True)
