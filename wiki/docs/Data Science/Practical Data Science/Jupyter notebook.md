---
title: Jupyter notebook
tags: [Jupyter Notebook]
---

The most visible changes to the language in Python 3 (honestly) are:

1. `print` is a command, not a statement (so you need parentheses)
2. `1/2` returns 0.5 (floating point), not 0 (integer); to get 0, you use the operation `1//2`


[Jupyter notebooks](http://www.jupyter.org) are a browser-based environment for writing code, interspersing code and Markdown, and displaying figures, all contained in "cells".

Launch jupyter via the command:

* `jupyter notebook` – launch notebook
* Then navigate to http://localhost:8888 (or possibly a later port number, if you have multiple notebooks open)


#### Cell magics

Magics are prefaced by `%` at the beginning of a line for *line magics* and `%%` at the beginning of a cell for *cell magics*.

A much more exhaustive list of magics is here: [Built-in cell magics](http://ipython.readthedocs.io/en/stable/interactive/magics.html).

* Time operations with `%timeit` (for single line), `%%timeit` (for the whole cell). This command will run the line or cell multiple times and provide average timing.

```Python
%time sum(x**2 for x in range(10000))
```
* Execute bash commands with %%bash.

```Python
%%bash
ls
```


#### Visualizations in notebook 

```Python
import matplotlib.pyplot as plt
%matplotlib notebook
%matplotlib inline
```