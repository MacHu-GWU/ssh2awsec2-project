# -*- coding: utf-8 -*-

if __name__ == "__main__":
    from ssh2awsec2.tests import run_cov_test

    run_cov_test(__file__, "ssh2awsec2", is_folder=True, preview=False)
