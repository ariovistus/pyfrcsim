
def theBool():
    return Bool.getDefaultInstance()


def theString():
    return String.getDefaultInstance()


def makeString(s: str):
    return String.newBuilder().setData(s).build()


def theFloat():
    return Float64.getDefaultInstance()


def makeFloat(f: float):
    return Float64.newBuilder().setData(f).build()
