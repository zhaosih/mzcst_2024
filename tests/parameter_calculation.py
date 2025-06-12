import mzcst_2024 as mz
from mzcst_2024 import Parameter, math_

if __name__ == "__main__":
    a = Parameter("a", "1")
    b = Parameter("b", "2")
    c = Parameter("c", "3")
    d = ((a + b) * c).rename("d")
    e = (a + b * c).rename("e")
    print(repr(d))
    print(repr(e))
    pass
