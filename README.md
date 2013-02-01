debug-tools
===========

Enhanced print statements for debugging.

 - Prints file path and line number
 - Prints the name of the variable as well as the value
 - Prints in color so it is easier to find

Dependencies
------------

[Blessings](http://pypi.python.org/pypi/blessings/) (for colorizing)

Install
-------

    pip install -e git://github.com/saltycrane/debug-tools.git#egg=debugtools

Usage
-----

To print the name of the current function:

    from debugtools import pfunc; pfunc()

To print the name and value of a variable (or expression):

    from debugtools import pvar; pvar('myvariable')

To print a string:

    from debugtools import prt; prt('1')

Tips
----

Add snippets [\[1\]][1] [\[2\]][2] [\[3\]][3] in your editor. Here is one of my Emacs snippets: [https://github.com/saltycrane/emacs/blob/master/snippets/text-mode/python-mode/pvar](https://github.com/saltycrane/emacs/blob/master/snippets/text-mode/python-mode/pvar)

[1]: http://manual.macromates.com/en/snippets
[2]: https://sublime-text-unofficial-documentation.readthedocs.org/en/latest/extensibility/snippets.html
[3]: https://github.com/capitaomorte/yasnippet
