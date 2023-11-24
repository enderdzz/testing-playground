import torch
import torch.nn
from rich.console import Console
con = Console()
package_list = ['torch', 'torch.nn', ]

for pkg in package_list:
    for api in dir(eval(pkg)):
        name = pkg+"."+api
        #if isinstance(eval(name), type): 
        if type(eval(name)) == type: # avoid duck typing.
            con.print(name, type(eval(name)), style="bold red")
        else:
            print(name, type(eval(name)))