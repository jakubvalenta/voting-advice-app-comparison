# Voting advice application comparison

Draw a graph comparing the voting advice applications of different countries.

Currently data for the 2019 election to the EU parliament for:

- Czech Republic
- Germany

## Installation

### Mac

``` shell
$ brew install python graphviz
$ pip install pipenv
$ make setup
```

### Arch Linux

``` shell
# pacman -S pipenv graphviz
$ make setup
```

### Other systems

Install these dependencies manually:

- Python 3.7
- pipenv
- graphviz

Then run:

``` shell
$ make setup
```

## Usage

### Generating the graph as PDF

```
$ make
```

The graph PDF will be created at `dist/graph.pdf`.

## Development

### Installation

``` shell
make setup-dev
```

### Linting

``` shell
make lint
```

### Help

``` shell
make help
```
