from contextlib import ContextDecorator
from pathlib import Path

import click
import yt_dlp


@click.command()
@click.option(
    "-P",
    "download_path",
    type=click.Path(file_okay=False, exists=True, path_type=Path),
    default=Path.cwd(),
    help="The paths where the files should be downloaded.  (this is just forwarded on to yt-dlp's -P option)",
)
def cli_main(download_path: Path):
    click.secho(f"Downloading to {download_path.absolute()}", fg="blue")
    click.secho("Starting download loop", fg="green", bold=True)
    while (url := input("enter url: ")) not in ["quit", "exit", "q"]:
        if not url.strip():
            print("\n" * 10)
            continue
        yt_dlp._real_main(["-P", str(download_path), "-f", "140", url])
        with (download_path / ".urls").open("ta") as f:
            print(url, file=f)
    click.secho("BYE", fg="green", bold=True)
