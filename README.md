# python-autologging
Python decorators for auto logging function and method calls

## Usage

```python
auto_logging = AutoLogging()
# constructor arguments options defaults are:
# logger=logging.getLogger(), handler=logs_composer.for_callable, loglevel=logging.INFO


@auto_logging.all_methods
class Foo:
    def fun(self, a, b='default value'):
        pass

    @staticmethod
    def stat_fun(a, b='default value'):
        pass

    @classmethod
    def cls_fun(cls, a, b='default value'):
        pass

# or

class X:
	pass

auto_logging.all_methods(X)


# ---

import my_functions

auto_logging.all_functions(my_functions)
```
