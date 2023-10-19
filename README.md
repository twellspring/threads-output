# threads-output
Python module to facilitate running multiple threads and keep the output separate

# Requires
```
pip install stdio-proxy
```

# Usage Example
```
#!/usr/bin/env python3

from time import sleep
from threads_output import ThreadManager


def my_function(sleep_time, header):
    print(f'OUTPUT {header}')
    sleep(sleep_time)
    print(f'done sleeping for {sleep_time} seconds')
    return f'RETURN {header}'

tmanager = ThreadManager()
tmanager.add('task1', my_function, 2, header="thing 1")
tmanager.add('task2', my_function, 7, "thing 2")
results = tmanager.run()
task1_return = tmanager.get_return('task1')
tmanager.print_output()

```
