
.. .. image:: https://readthedocs.org/projects/ssh2awsec2/badge/?version=latest
    :target: https://ssh2awsec2.readthedocs.io/en/latest/
    :alt: Documentation Status

.. image:: https://github.com/MacHu-GWU/ssh2awsec2-project/workflows/CI/badge.svg
    :target: https://github.com/MacHu-GWU/ssh2awsec2-project/actions?query=workflow:CI

.. .. image:: https://codecov.io/gh/MacHu-GWU/ssh2awsec2-project/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/MacHu-GWU/ssh2awsec2-project

.. image:: https://img.shields.io/pypi/v/ssh2awsec2.svg
    :target: https://pypi.python.org/pypi/ssh2awsec2

.. image:: https://img.shields.io/pypi/l/ssh2awsec2.svg
    :target: https://pypi.python.org/pypi/ssh2awsec2

.. image:: https://img.shields.io/pypi/pyversions/ssh2awsec2.svg
    :target: https://pypi.python.org/pypi/ssh2awsec2

.. image:: https://img.shields.io/badge/Release_History!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/ssh2awsec2-project/blob/main/release-history.rst

.. image:: https://img.shields.io/badge/STAR_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/ssh2awsec2-project

------

.. .. image:: https://img.shields.io/badge/Link-Document-blue.svg
    :target: https://ssh2awsec2.readthedocs.io/en/latest/

.. .. image:: https://img.shields.io/badge/Link-API-blue.svg
    :target: https://ssh2awsec2.readthedocs.io/en/latest/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
    :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
    :target: https://github.com/MacHu-GWU/ssh2awsec2-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
    :target: https://github.com/MacHu-GWU/ssh2awsec2-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
    :target: https://github.com/MacHu-GWU/ssh2awsec2-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
    :target: https://pypi.org/pypi/ssh2awsec2#files


Welcome to ``ssh2awsec2`` Documentation
==============================================================================
``ssh2awsec2`` is a interactive Python CLI tool to help you SSH to your EC2 instances smoothly.

.. code-block:: bash

    +----- ⏱ 🟢 Start 'SSH to EC2 instance' ----------------------------------------+
    |
    | Which EC2 you want to SSH to?
    | ⬆ ⬇ Move your cursor up and down and press Enter to select.
    [?] Current selection: id = i-0123456789aaaaaaa, name = 'jump-host', public ip = 111.111.111.111
     > id = i-0123456789aaaaaaa, name = 'jump-host', public ip = 111.111.111.111
       id = i-0123456789bbbbbbb, name = 'dev-box', public ip = 222.222.222.222
       id = i-0123456789ccccccc, name = 'web-app', public ip = 333.333.333.333

    | ✅ selected: id = i-0123456789aaaaaaa, name = 'jump-host', public ip = 111.111.111.111
    | try to locate pem file ...
    | ✅ found pem file at: /Users/myname/ec2-pem/111122223333/us-east-1/dev.pem
    | Try to find OS username based on the AMI id = ami-0123456789abcdefg, name = ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server
    | cannot automatically detect OS username
    | Choose OS username of your EC2, if you don't know, see this document: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/connection-prereqs.html#connection-prereqs-get-info-about-instance
    | ⬆ ⬇ Move your cursor up and down and press Enter to select.
    [?] Current selection: ubuntu
       ec2-user
     > ubuntu
       fedora
       centos
       admin
       bitnami
       root

    | Run ssh command: ssh -i /Users/myname/ec2-pem/111122223333/us-east-1/dev.pem ubuntu@111.111.111.111
    | Precess Ctrl + D to exit SSH session
    Welcome to Ubuntu 20.04.6 LTS (GNU/Linux 5.15.0-1031-aws x86_64)

     * Documentation:  https://help.ubuntu.com
     * Management:     https://landscape.canonical.com
     * Support:        https://ubuntu.com/advantage

      System information as of Wed Jun 14 23:28:41 UTC 2023

      System load:  0.0                Processes:             104
      Usage of /:   52.0% of 19.20GB   Users logged in:       0
      Memory usage: 7%                 IPv4 address for ens5: 10.1.1.1
      Swap usage:   0%

     * Ubuntu Pro delivers the most comprehensive open source security and
       compliance features.

       https://ubuntu.com/aws/pro

     * Introducing Expanded Security Maintenance for Applications.
       Receive updates to over 25,000 software packages with your
       Ubuntu Pro subscription. Free for personal use.

         https://ubuntu.com/aws/pro

    Expanded Security Maintenance for Applications is not enabled.

    19 updates can be applied immediately.
    To see these additional updates run: apt list --upgradable

    Enable ESM Apps to receive additional future security updates.
    See https://ubuntu.com/esm or run: sudo pro status


    The list of available updates is more than a week old.
    To check for new updates run: sudo apt update
    New release '22.04.2 LTS' available.
    Run 'do-release-upgrade' to upgrade to it.


    2 updates could not be installed automatically. For more details,
    see /var/log/unattended-upgrades/unattended-upgrades.log

    Last login: Wed Jun 14 23:23:58 2023 from 100.100.100.100
    ubuntu@ip-10-1-1-1:~$ logout
    Connection to 111.111.111.111 closed.
    |
    +----- ⏰ 🟢 End 'SSH to EC2 instance', elapsed = 16.35 sec ---------------------+

**Usage Example**

.. code-block:: bash

    # show CLI help info
    ssh2awsec2

    # or use the short name
    sshec2

For first usage, you need to configure ``ssh2awsec2`` to locate your `AWS CLI credential <https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html>`_.

.. code-block:: bash

    # show config related information
    sshec2 info

    # show config subcommand help info
    sshec2 config

    # show current config
    sshec2 config show

    # set the AWS profile
    sshec2 config set-profile --profile <your_aws_profile>

    # set to use the default AWS profile
    sshec2 config set-profile --profile default

    # set cache expire time
    sshec2 config set-cache-expire 3600

    # clear cache
    sshec2 clear-cache

Then you can use ``sshec2 ssh`` command to ssh to your AWS EC2 instance. Just follow the interactive prompt:

.. code-block:: bash

    # show help info
    sshec2 ssh --help

    # pick an EC2 and ssh into it
    sshec2 ssh

    # you can use -n to filter EC2 by name tag
    sshec2 ssh -n <name_tag_here>
    # example
    sshec2 ssh -n jump_host

    # you can use -i to filter EC2 by instance id
    sshec2 ssh -i <full_instance_id_or_chunk_here>
    # example
    sshec2 ssh -i 1a2b

    # you can use -k to filter EC2 by instance id (quote the query string)
    sshec2 ssh -k "<name_tag_key_value_pair_here>"
    # example
    sshec2 ssh -k "env=prod,owner=alice"

It prompt you to select EC2 instance and probably ask for the OS username. The selection will be cached for 24 hours, so you will see it on top of the list next time.


.. _install:

Install
------------------------------------------------------------------------------

``ssh2awsec2`` is released on PyPI, so all you need is:

.. code-block:: console

    $ pip install ssh2awsec2

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade ssh2awsec2