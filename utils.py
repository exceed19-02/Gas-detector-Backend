from typing import List


def get_average_status(all_status: List[str]) -> str:
    """"""
    status_dct = {"SAFE": 0, "WARNING": 1, "DANGER": 2, "WARN": 1}

    status_sum = []
    for status in all_status:
        status_sum.append(status_dct[status])

    average_status = round(sum(status_sum) / len(status_sum))

    return list(status_dct.keys())[average_status]
