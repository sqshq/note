---
title: Records
toc: true
date: 2017-12-30
top: 3
---

#### Get key name from Python KeyError exception

```Python
try:
    x2 = myDict['key2']
except KeyError as e:    
    print e.args[0]
```

#### How to print without newline or space?

```python
print('.', end='')
```

#### String r

`r` is a prefix for string *literals*. This means, r"1\2\3\4" will not interpret \ as an escape when creating the string value, but keep \ as an actual character in the string. Thus, r"1\2\3\4" will have seven characters.

`var = "1\2\3\4"` will interpret backslashes as escapes, create the string `'1\x02\x03\x04'` (a four-character string), then assign this string to the variable `var`.

#### 程序暂停

```Python
import time
time.sleep(amount) #单位s
```

#### 捕获ctrl-C

使用`KeyboardInterrupt`捕获异常[ref](https://stackoverflow.com/questions/15318208/capture-control-c-in-python).

```python
try:
    # DO THINGS
except KeyboardInterrupt:
    # quit
    sys.exit()
```

