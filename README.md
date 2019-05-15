# Voting advice application comparison

This is a chart comparing the voting advice applications for the **2019 European
Parliament election** of:

&#x1f1e8;&#x1f1ff; Czech Republic ([Volební kalkulačka EP
2019](https://volebnikalkulacka.cz/cs/evropsky-parlament-2019/) by
[KohoVolit.eu](http://kohovolit.eu/))\
&#x1f1e9;&#x1f1ea; Germany ([Wahl-O-Mat zur Europawahl
2019](https://www.wahl-o-mat.de/europawahl2019/) by [Bundeszentrale für
politische Bildung](https://www.bpb.de/))

The **English translations and similarity classifications** (connections between
the questions) are original work. This information was **not provided by the
authors of the voting advice apps** and might therefore be inaccurate.

Please refer to the websites of the voting advice apps to learn about the
**method** used to choose the questions:

- [VolebníKalkulačka.cz - Info](https://volebnikalkulacka.cz/info/)
- [Wahl-O-Mat zur Europawahl 2019 - FAQ](https://www.wahl-o-mat.de/europawahl2019/popup_faq.php)

There is a second voting advice app in the Czech Republic - [Volební kalkulačka
by Programy do
Voleb](https://eu2019.programydovoleb.cz/volebni-kalkulacka). This one was not
chosen for the comparison because it does not publish any information on the
method used to choose the questions.

![Comparison of the Czech and German voting advice applications for the 2019
European Parliament election](./dist/graph.svg)

Legend:

- **gray background**: unique question
- **solid line** connection: very similar questions
- **dashed line** connection: related questions

License:

This chart image is licensed under the [Creative Commons Attribution-ShareAlike
4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/).

## Drawing the chart

### Installation

#### Mac

``` shell
$ brew install python graphviz
$ pip install pipenv
$ make setup
```

#### Arch Linux

``` shell
# pacman -S pipenv graphviz
$ make setup
```

#### Other systems

Install these dependencies manually:

- Python 3.7
- pipenv
- graphviz

Then run:

``` shell
$ make setup
```

### Usage

#### Rendering the chart as SVG

```
$ make
```

The chart SVG will be created at `dist/graph.svg`.

### Development

#### Installation

``` shell
make setup-dev
```

#### Linting

``` shell
make lint
```

#### Help

``` shell
make help
```

### Contributing

**Feel free to remix this project.**

The code is licensed under the [Apache License, Version
2.0](http://www.apache.org/licenses/LICENSE-2.0).

The translations of the questions of the voting advice apps and the chart image
are licensed under the [Creative Commons Attribution-ShareAlike 4.0
International License](http://creativecommons.org/licenses/by-sa/4.0/).
