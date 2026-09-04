.. SPDX-License-Identifier: GPL-2.0

Checking for needed translation updates
=======================================

This script helps track the translation status of the documentation in
different locales, i.e., whether the documentation is up-to-date with
the English counterpart.

How it works
------------

The script searches the translated file's history, from newest to oldest, for
a commit message recording the English commit used as its baseline.  Baseline
markers such as ``Update to commit HASH`` are checked against the corresponding
English file before being used.  Thus, later translation-only edits such as
typo fixes do not make an outdated translation appear current.  For older
translation histories without an explicit marker, the script falls back to
inferring a baseline from author dates.

After finding a valid baseline, the script reports non-merge commits which
modified the English file between that baseline and HEAD.  Both translated
files and translated directories can be supplied.  Explicit paths outside
``Documentation/translations/<locale>/`` are rejected with an error.

Features implemented

-  check all files in a certain locale
-  check a single file or a set of files
-  provide options to change output format
-  track the translation status of files that have no translation

Usage
-----

::

   tools/docs/checktransupdate.py --help

Please refer to the output of argument parser for usage details.

Samples

-  ``tools/docs/checktransupdate.py -l zh_CN``
   This will print all the files that need to be updated in the zh_CN locale.
-  ``tools/docs/checktransupdate.py Documentation/translations/zh_CN/dev-tools/testing-overview.rst``
   This will only print the status of the specified file.
-  ``tools/docs/checktransupdate.py Documentation/translations/zh_CN/dev-tools``
   This will recursively print the status of translated files in the specified
   directory.

Then the output is something like:

::

    Documentation/dev-tools/kfence.rst
    No translation in the locale of zh_CN

    Documentation/translations/zh_CN/dev-tools/testing-overview.rst
    commit 42fb9cfd5b18 ("Documentation: dev-tools: Add link to RV docs")
    1 commits needs resolving in total
