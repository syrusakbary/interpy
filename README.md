# Interpy = Python String Interpolation
Interpy **extends Python** to support *Ruby like* string interpolation **#{}**. Quick example: `print "Hello #{your_name}"`

It is **hightly optimized**, and directly compiled to bytecode, so you will have the same Python speed when using it.

## Installation

The installation of this package is quite simple, you only have to run `pip install interpy`.

## Usage

All python files with string interpolation must have the following first line

```python
# coding: interpy
```

Example:

```python
# coding: interpy

package = "Interpy"
print "Enjoy #{package}!"
```

## How it works
*This package is inspired in Dropbox [pyxl template engine](https://github.com/dropbox/pyxl).*


### Parsing

Interpy uses support for specifying source code encodings as described in [PEP 263](http://www.python.org/dev/peps/pep-0263/) to do what it does. The functionality was originally provided so that python developers could write code in non-ascii languages (eg. chinese variable names). Interpy creates a custom encoding called interpy which allows it to convert interpolated strings into regular python before the file is compiled. Once the interpy codec is registered, any file starting with `# coding: interpy` is run through the interpy parser before compilation.


### Compiling

The above example would be compiled to this (in *bytecode*):

```python
# coding: interpy

package = "Interpy"
print "Enjoy "+str(package)+"!"
```

## Compatibility

This package is fully compatible with Python 2+, Python 3+ and PyPy


## Why?

I really enjoyed Ruby String interpolation, and `"".format(...)` or `"" % (...)` seems very verbose to me.
*I'm lazy by nature* ;)
