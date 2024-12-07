# Static Site Generator

## Usage
Clone the project, and run `main.sh &` (backgrounding is recommended
since the script launches Python's HTTP server.)

To view the generated site, visit `localhost:8888`.

## Known Bugs
- Code listings are formatted in the same manner as the rest of the
text.

- To truly stop `main.sh` in the case where you've backgrounded it,
  you must foreground it first with `fg`, then type `Control-C`.
