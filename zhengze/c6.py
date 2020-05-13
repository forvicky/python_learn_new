# 组

import re

a = 'PythonPythonPythonPythonPython'

# ()是且关系，表示一组
r = re.findall('(Python){3}', a)
