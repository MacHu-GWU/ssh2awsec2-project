# -*- coding: utf-8 -*-
import pytest

from ssh2awsec2.pem_file import PemFileStore


class TestPemFileStore:
    def test(self):
        pem_file_store = PemFileStore()

        aws_account_id = "123456789012"
        aws_account_alias = "my-aws-account-alias"
        aws_region = "us-east-1"
        key_name = "my-key-pair"
        path_pem_file = pem_file_store.get_pem_file_path(
            account_id_or_alias=aws_account_id,
            region=aws_region,
            key_name=key_name,
        )
        path_pem_file.unlink(missing_ok=True)

        with pytest.raises(FileNotFoundError):
            pem_file_store.locate_pem_file(
                region=aws_region,
                key_name=key_name,
                account_id=aws_account_id,
                account_alias=None,
            )

        with pytest.raises(FileNotFoundError):
            pem_file_store.locate_pem_file(
                region=aws_region,
                key_name=key_name,
                account_id=None,
                account_alias=aws_account_alias,
            )

        path_pem_file.parent.mkdir(parents=True, exist_ok=True)
        path_pem_file.write_text("this is a dummy pem file")

        pem_file_store.locate_pem_file(
            region=aws_region,
            key_name="my-key-pair",
            account_id=aws_account_id,
            account_alias=None,
        )
        pem_file_store.locate_pem_file(
            region=aws_region,
            key_name="my-key-pair.pem",
            account_id=aws_account_id,
            account_alias=None,
        )



if __name__ == "__main__":
    from ssh2awsec2.tests import run_cov_test

    run_cov_test(__file__, "ssh2awsec2.pem_file", preview=False)
