import webbrowser
from pathlib import Path

import click
import yt_dlp


@click.command()
@click.option(
    "-P",
    "download_path",
    type=click.Path(file_okay=False, path_type=Path),
    default=Path.cwd(),
    help="The paths where the files should be downloaded.  (this is just forwarded on to yt-dlp's -P option)",
)
@click.option("--web", is_flag=True, help="Don't download, instead open previously downloaded stuff in a web browser")
@click.pass_context
def cli_main(ctx: click.Context, download_path: Path, web: bool):
    if web:
        click.secho(f"Processing urls from {download_path.absolute()}", fg="blue")
        with (download_path / ".urls").open("rt") as f:
            urls = f.read().splitlines()
        for i, url in enumerate(urls, start=1):
            click.secho(f"{i}/{len(urls)}: {url}")
            resp = input(f"open [n/Y] ? ").lower()
            if resp in ["yes", "y", ""]:
                webbrowser.open(url)
            if resp in ["quit", "exit", "q"]:
                break
        ctx.exit(0)
    if not download_path.exists():
        if click.confirm(f"{download_path} does not exist; Create it?", default=True):
            download_path.mkdir(parents=True)
        else:
            click.secho("Bailing")
            ctx.exit(0)
    click.secho(f"Downloading to {download_path.absolute()}", fg="blue")
    click.secho("Starting download loop", fg="green", bold=True)
    while (url := input(click.style("enter url: ", fg="blue", bold=True))) not in ["quit", "exit", "q"]:
        if not url.strip():
            print("\n" * 10)
            continue
        yt_dlp._real_main(["-P", str(download_path), "-f", "140", "--embed-metadata", url])
        with (download_path / ".urls").open("ta") as f:
            print(url, file=f)
    click.secho("BYE", fg="green", bold=True)
