import typer

from config import CONFIG, Config
from game import Game

app = typer.Typer()


def run_game_with_config(
    min_speed: int,
    max_speed: int,
    fps: int,
    font_path: str,
    gui_font_size: int,
    bg_color: str,
    gui_text_color: str,
):
    config = CONFIG.parse_cli(
        min_speed=min_speed,
        max_speed=max_speed,
        fps=fps,
        font_path=font_path,
        gui_font_size=gui_font_size,
        gui_text_color=gui_text_color,
        bg_color=bg_color,
    )
    run_game(config)


def level(min_speed: int, max_speed: int, name: str, help_text: str):
    def decorator(func):
        @app.command(name=name, help=help_text)
        def wrapper(
            fps: int | None = typer.Option(None, "--fps"),
            font_path: str | None = typer.Option(None, "--font-path"),
            gui_font_size: int | None = typer.Option(None, "--gui-font-size"),
            bg_color: str | None = typer.Option(None, "--bg-color"),
            gui_text_color: str | None = typer.Option(
                None, "--gui-text-color"
            ),
        ):
            run_game_with_config(
                min_speed,
                max_speed,
                fps,
                font_path,
                gui_font_size,
                bg_color,
                gui_text_color,
            )

        return wrapper

    return decorator


@level(1, 4, name="easy", help_text="Лёгкий уровень: min_speed=1, max_speed=4")
def easy():
    pass


@level(
    3, 6, name="medium", help_text="Средний уровень: min_speed=3, max_speed=6"
)
def medium():
    pass


@level(
    5, 8, name="hard", help_text="Сложный уровень: min_speed=5, max_speed=8"
)
def hard():
    pass


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    min_speed: int | None = typer.Option(None, "--min-speed"),
    max_speed: int | None = typer.Option(None, "--max-speed"),
    fps: int | None = typer.Option(None, "--fps"),
    font_path: str | None = typer.Option(None, "--font-path"),
    gui_font_size: int | None = typer.Option(None, "--gui-font-size"),
    bg_color: str | None = typer.Option(None, "--bg-color"),
    gui_text_color: str | None = typer.Option(None, "--gui-text-color"),
):
    if ctx.invoked_subcommand is None:
        config = CONFIG.parse_cli(
            min_speed=min_speed,
            max_speed=max_speed,
            fps=fps,
            font_path=font_path,
            gui_font_size=gui_font_size,
            gui_text_color=gui_text_color,
            bg_color=bg_color,
        )
        run_game(config)


def run_game(config: Config):
    with Game(config) as game:
        game.run()


if __name__ == "__main__":
    app()
