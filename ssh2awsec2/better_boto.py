# -*- coding: utf-8 -*-

import typing as T


def get_account_id(sts_client) -> T.Optional[str]:
    try:
        return sts_client.get_caller_identity()["Account"]
    except Exception:
        return None


def get_account_alias(iam_client) -> T.Optional[str]:
    try:
        res = iam_client.list_account_aliases()
        return res.get("AccountAliases", [None])[0]
    except Exception as e:  # pragma: no cover
        if "AccessDenied" in str(e):
            return None
        else:
            raise e
