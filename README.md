# Simple target practice game

[Course link](https://stepik.org/course/293307)

### Commands
- Run game directly with awailable CLI parameters
- Or select difficulty with subcommands

### Parameters
- min_speed
- max_speed
- fps
- gui_font_size
- gui_text_color
- bg_color
- etc.

### Subcommands
- easy
- medium
- hard

### Usage
```
uv run main.py

uv run main.py --min-speed 5 --max-speed 10

uv run main.py easy --fps 120

uv run main.py medium --fps 120

uv run main.py hard
```