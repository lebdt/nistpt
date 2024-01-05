modules = ['panes', 'menu']

for module in modules:
    exec(f"from .{module} import *")
