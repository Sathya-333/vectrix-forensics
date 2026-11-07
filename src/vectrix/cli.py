import typer
from rich.console import Console

from vectrix import __version__

app = typer.Typer(
    name="vectrix",
    help="Build execution forensics and supply-chain investigation engine.",
    no_args_is_help=True,
)

console = Console()


@app.callback()
def main():
    """VECTRIX forensic engine."""



@app.command()
def version():
    """Display VECTRIX version."""
    console.print(f"[bold cyan]VECTRIX[/bold cyan] v{__version__}")


if __name__ == "__main__":
    app()