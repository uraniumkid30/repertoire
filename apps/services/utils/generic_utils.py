import os
import re
import time
import logging
import functools
import traceback


def timer(func):
    """
    this helps to decorate a function with timing functionality

    Parameters
    ----------
    func : function object
        funnction to be decorated
    """

    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        logger = kwargs.get("logger")
        if logger is None:
            logger = logging.getLogger("integrations")
        elif isinstance(logger, str):
            logger = logging.getLogger(logger)
        tic = time.perf_counter()
        value = func(*args, **kwargs)
        toc = time.perf_counter()
        elapsed_time = toc - tic
        logger.info(f"Decorator Elapsed time: {elapsed_time:0.4f} seconds")
        return value

    return wrapper_timer


def dynamic_filter(
    unfiltered_list,
    match_field="",
    match_string="",
    items_to_match={},
    find_non_matching_items=False,
    use_regex_matching=False,
):
    """
    customized filter object, used to filter a list or tuple of objects
    (mainly dictionaries) so as to select an object that meets a criteria.

    Parameters
    ----------
    target_list : container (list,tuple)
        list of dictionary objects

    Default Arguments
    -----------------
    key_string : immutable
        field name or key of the dictionary
    search_string : object
        value searched for
    source_dict : dictionary
        all key and value pair searched for
    negative_use : boolean
        uses unequal comparison

    Returns
    -------
    returns : filter Object
        result from filter criteria
    """

    def iterator_function(unfiltered_list_item):
        if items_to_match:
            target_set = set(unfiltered_list_item)
            items_to_match_set = set(items_to_match)
            common_items = target_set.intersection(items_to_match_set)
            if find_non_matching_items:
                matches_found = set(
                    _key
                    for _key in common_items
                    if (unfiltered_list_item[_key] != items_to_match[_key])
                )
            else:
                matches_found = set(
                    _key
                    for _key in common_items
                    if unfiltered_list_item[_key] == items_to_match[_key]
                )
            if len(matches_found) == len(items_to_match):
                return True
        else:
            for _key, _value in unfiltered_list_item.items():
                if find_non_matching_items:
                    if not use_regex_matching or (
                        not isinstance(match_string, str) or not isinstance(_value, str)
                    ):
                        if (match_field == _key) and (match_string != _value):
                            return True
                    elif use_regex_matching and (
                        isinstance(match_string, str) and isinstance(_value, str)
                    ):
                        if (match_field == _key) and (
                            not re.search(match_string, _value)
                        ):
                            return True
                else:
                    if not use_regex_matching or (
                        not isinstance(match_string, str) or not isinstance(_value, str)
                    ):
                        if (match_field == _key) and (match_string == _value):
                            return True
                    elif use_regex_matching and (
                        isinstance(match_string, str) and isinstance(_value, str)
                    ):
                        if (match_field == _key) and re.search(match_string, _value):
                            return True
        return False

    return filter(iterator_function, unfiltered_list)
