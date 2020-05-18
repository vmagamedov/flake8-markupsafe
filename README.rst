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

WebHelpers support
~~~~~~~~~~~~~~~~~~

This plugin also checks for ``webhelpers.html.literal()`` usages. But there is
a known issue that SQLAlchemy has it's own ``sqlalchemy.literal()``, this may
cause false positives.

i18n support
~~~~~~~~~~~~

This plugin has an exception for a functions called ``_`` and ``*gettext``. You
can pass result of these functions to the ``Markup``, but their arguments should
be also safe.

.. code-block:: python

  Markup(_("<script>{}</script>")).format(code)

Mako support
~~~~~~~~~~~~

Note: Mako should be installed to use this feature.

.. code-block:: console

  $ python -m flake8_markupsafe.mako --show-source ./examples
  examples/view.mako:3
      unsafe = Markup('<script>{}</script>'.format(value))
  examples/view.mako:8
      <div class="unsafe">${Markup('<script>{}</script>'.format(value))}</div>

Known to be safe
~~~~~~~~~~~~~~~~

Here is how to ignore errors in a Python code:

.. code-block:: python

  title = Markup(page.title)  # noqa: MS001

Here is how to ignore errors in a Mako templates:

.. code-block:: mako

  <%
      title = Markup(page.title)  # noqa
  %>

.. _Flake8: https://flake8.pycqa.org/
.. _MarkupSafe: https://markupsafe.palletsprojects.com/
