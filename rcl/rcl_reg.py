import re

with open('rcl_reg.txt', 'r') as rcl_regex_string:
  with open('rcl_reg_test_data.txt', 'r') as rcl_test_string:
    rcl_regex = re.search( f'({rcl_regex_sring})', rcl_test_string)    
    print(result.groups())
