"""Module That Tests the RCL Regex against the Test Data."""

import re

with open('rcl_reg.txt', 'r', encoding="utf-8") as rcl_regex_string:
    with open('rcl_reg_test_data.txt', 'r', encoding="utf-8") as rcl_test_string:
        result = re.search( f'({rcl_regex_string})', rcl_test_string)
        print(result.groups())
