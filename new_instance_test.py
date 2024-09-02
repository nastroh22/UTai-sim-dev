# NOTE Q: is pyjulia config a one-time thing?

from julia import Julia
jl = Julia(compiled_modules=False)
from julia import HelloWorld as hello

# NOTE: answer -> No, we have to re-run setup everytime
# TODO: kind of annoying, is there a workaround ??

# NOTE: that will be especially bad for pre-compiling tons of dependencies