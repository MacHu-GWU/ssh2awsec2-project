.. _release_history:

Release and Version History
==============================================================================


X.Y.Z (Backlog)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


0.1.2 (2024-06-19)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Bugfixes**

- Fix a bug that it try to detect default system user based on AMI even when it does not exist.

**Miscellaneous**

- Only support Python3.8+, because the core dependency ``inquirer`` only support Python3.8+.
- Add support for Python3.12.


0.1.1 (2023-06-14)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- first working version.
- add the ``sshec2 ssh``, interactive ssh command.
- add the following cli commands:
    - ``sshec2 ssh``
    - ``sshec2 info``
    - ``sshec2 clear-cache``
    - ``sshec2 config show``
    - ``sshec2 config set-profile``
    - ``sshec2 config set-region``
    - ``sshec2 config set-cache-expire``


0.0.1 (2023-06-13)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- First release
- Release as a placeholder on PyPI.
