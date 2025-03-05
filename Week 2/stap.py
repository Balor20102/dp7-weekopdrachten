class Stap:
    def __init__(self, stap, tip):
        self.stap = str(stap)
        self.tip = str(tip)

    def __str__(self):
        return f"stap is: {self.stap}"