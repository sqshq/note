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