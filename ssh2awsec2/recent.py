# -*- coding: utf-8 -*-

"""
As a CLI app, it prompt to select from multiple choice. We want to remember
the recent choice and use it as the default choice next time.
"""

import typing as T
import uuid
import dataclasses

from collections import deque
import inquirer

from .cache import cache
from .config import RECENT_CACHE_EXPIRE


@dataclasses.dataclass
class ListChoices:
    """
    A utility class that prompt to select from multiple choice. It remembers
    the recent choice and use it as the default choice next time.

    :param key: the unique Key for this choice.
    """

    key: str = dataclasses.field()
    expire: int = dataclasses.field(default=RECENT_CACHE_EXPIRE)
    max_item: int = dataclasses.field(default=20)

    def save_selected_choice(
        self,
        id: str,
        value: str,
    ):
        """
        Save the selected choice to cache.

        :param id: id of selected choice
        :param value: value of selected choice
        """
        q: T.Optional[T.Deque[T.Tuple[str, str]]] = cache.get(self.key)
        if q is None:
            q = deque(maxlen=self.max_item)
        q.appendleft((id, value))
        cache.set(self.key, q, expire=self.expire)

    def read_recent_choices(self) -> T.Deque[T.Tuple[str, str]]:
        """
        Get recently selected cache from cache.
        """
        q: T.Optional[T.Deque[T.Tuple[str, str]]] = cache.get(self.key)
        if q is None:
            q = deque(maxlen=self.max_item)
        return q

    def clear_cache(self):
        """
        Delete the cached recent choices.
        """
        cache.delete(self.key)

    def ask(
        self,
        message: str,
        choices: T.Dict[str, str],
        merge_selected: bool = False,
    ) -> T.Tuple[str, str]:  # pragma: no cover
        """
        Prompt to select from multiple choice, and return the selected choice
        id and value. It remembers the recent choice and use it as the default
        choice next time.

        :param message: the message of the prompt
        :param choices: the id / value pair of all choices
        :param merge_selected: if True, then the recently selected choices
            will be merged into the choices. If False, then only the given
            choices will prompt.

        :return: the selected choice id and value
        """
        # prepare id to value and value to id mapper
        mapper = choices
        reversed_mapper = {v: k for k, v in choices.items()}

        # read recently selected choices
        q = self.read_recent_choices()

        # sort the choices based on the recently selected choices
        sorted_mapper = dict()
        if merge_selected:
            for selected_id, selected_value in q:
                sorted_mapper[selected_id] = selected_value
                reversed_mapper[selected_value] = selected_id
        else:
            for selected_id, _ in q:
                if selected_id in mapper:
                    sorted_mapper[selected_id] = mapper[selected_id]

        for id, value in mapper.items():
            sorted_mapper.setdefault(id, mapper[id])

        # send the inquirer prompt
        name = uuid.uuid4().hex
        questions = [
            inquirer.List(
                name,
                message=message,
                choices=list(sorted_mapper.values()),
            ),
        ]

        # collect answer and update cache
        answers = inquirer.prompt(questions)
        selected_value = answers[name]
        selected_id = reversed_mapper[selected_value]
        self.save_selected_choice(selected_id, selected_value)

        return selected_id, selected_value
