flake8-markupsafe
=================

Flake8_ plugin to check for unsafe MarkupSafe_ usage in your code to prevent XSS
vulnerabilities.

Installation
~~~~~~~~~~~~

.. code-block:: console

  $ pip3 install https://github.com/vmagamedov/flake8-markupsafe/archive/master.zip

Example
~~~~~~~

.. code-block:: console

  $ flake8 --show-source ./examples
  ./examples/view.py:14:12: MS001 Markup is used in a dangerous way
      return Markup("<script>{}</script>".format(value))
             ^
  ./examples/view.py:18:12: MS001 Markup is used in a dangerous way
      return Markup(gettext("<script>{}</script>".format(value)))
             ^

Mako support
~~~~~~~~~~~~

.. code-block:: console

  $ python -m flake8_markupsafe.mako --show-source ./examples
  examples/view.mako:3
      unsafe = Markup('<script>{}</script>'.format(value))
  examples/view.mako:8
      <div class="unsafe">${Markup('<script>{}</script>'.format(value))}</div>

.. _Flake8: https://flake8.pycqa.org/
.. _MarkupSafe: https://markupsafe.palletsprojects.com/
