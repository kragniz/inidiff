inidiff
=======

.. image:: https://travis-ci.org/kragniz/inidiff.png
   :target: https://travis-ci.org/kragniz/inidiff
   :alt: Latest Travis CI build status

Find the differences between two ini config files.

Usage
-----

.. code-block:: bash

    $ inidiff some_file.ini some_newer_file.ini
    [hello]
    -thing=b
    +thing=c
    [df]
    -dfd=fd


Installation
------------

.. code-block:: bash

    $ pip install inidiff
