# habit-cli

A simple habit tracker.

![demo](https://github.com/bunchesofdonald/habit-cli/blob/master/demo.svg)


## Installation

```sh
pip install --upgrade --src="$HOME/.src" -e git+https://github.com/bunchesofdonald/habit-cli@master#egg=habit-cli
```

## Usage

```sh
$ hb --help
Usage: hb [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  add   Add a habit to track
  list  List all known habits
  log   Mark a habit as complete for the day
  show  Show progress on habits for the day
```
