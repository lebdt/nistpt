modules = ['session', 'tables']

for module in modules:
    exec(f"from .{module} import *")
