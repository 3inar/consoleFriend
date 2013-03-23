from main import Console

# this is an example of a two-command implementation of Console
class TestShell(Console):
    def __init__(self):
        Console.__init__(self, prompt = "<3<3<3", commands = ["echo", "add"])

    def add(self, a, b):
        ans = int(a) + int(b)
        print ans

    def echo(self, *args):
        print ' '.join(args)

if __name__ == "__main__":
    c = TestShell()
    c.run()

