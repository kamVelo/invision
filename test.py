class a:
    def __init__(self):
        self.poop = "poo"
        self.b = b(self)

class b:
    def __init__(self, poo:a):
        print(poo.poop)
x = a()