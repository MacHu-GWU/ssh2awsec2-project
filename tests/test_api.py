# -*- coding: utf-8 -*-

from ssh2awsec2 import api


def test():
    _ = api.get_account_id
    _ = api.get_account_alias
    _ = api.get_boto_ses
    _ = api.Config
    _ = api.PemFileStore
    _ = api.ListChoices


if __name__ == "__main__":
    from ssh2awsec2.tests import run_cov_test

    run_cov_test(__file__, "ssh2awsec2.api", preview=False)
