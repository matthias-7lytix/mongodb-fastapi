import typer
import uvicorn

app = typer.Typer()


@app.command()
def stop():
    print("stop")


@app.async_command()
async def start(
    host: str = typer.Option(
        "localhost",
        help="host to launch the app"
    ),
    port: int = typer.Option(
        8000,
        help="port, where app is listening"
    )
):
    """Start the app."""
    typer.echo("Start APP at '%s:%d" % (host, port))
    config = uvicorn.Config("app.main:app", log_level="info",
                            port=port, host=host)
    server = uvicorn.Server(config)
    await server.serve()
