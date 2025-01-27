.. _changelog:

Change log
==========

Next version
~~~~~~~~~~~~

- Added pre-commit.
- Switched to a declarative setup.
- Added GitHub actions.
- Renamed the main branch.
- Changed ``OembedContent.render`` to return a tuple. Raised the minimum
  FeinCMS version to 22.0.
- Dropped Python 3.8, Django 3.2.
- Added Django 4.2, 5.2 and Python 3.12, 3.13.
- Removed the FeinCMS dependency in the package, only the tests depend on it.


v1.5.0 (2020-01-22)
~~~~~~~~~~~~~~~~~~~

- Reformatted the code using black.
- Changed ``FeedContent.render`` to return ``(template, context)``
  instead of rendering the template itself. This raises the minimum
  FeinCMS version to v1.15.
- Updated the code to work with Django 2 and 3.
- Added a minimal testsuite after 10 years.
