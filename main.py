import readline
from sys import stdout

class Console():
    def __init__(self, prompt = '#', commands = []):
        # commands is a whitelist of methods you are allowed to call
        if 'quit' not in commands:
            commands.append('quit')
        if 'help' not in commands:
            commands.append('help')

        ignore_list = dir(self)
        self.ignore_list = filter(lambda a: a not in commands, ignore_list)
        self.options = sorted(commands)
        self.prompt = prompt + ' '
        self.running = True

    class Completer():
        def __init__(self, keywords):
            self.options = sorted(keywords)
        def complete(self, text, state):
            response = None

            # state == 0 means there is no match list, make one
            if state == 0:
                if text:
                    self.matches = [s
                                    for s in self.options
                                    if s and s.startswith(text)]
                else:
                    self.matches = self.options[:]
            try:
                response = self.matches[state]
            except IndexError:
                response = None
            return response

    def run(self):
        readline.parse_and_bind('tab: complete')
        readline.set_completer(self.Completer(self.options).complete)
        self.usage()
        while self.running:
            try:
                line = raw_input(self.prompt)
            except EOFError:
                stdout.write(''.join(["\r", self.prompt, "quit\n"]))
                stdout.flush()
                self._quit()
                continue
            except KeyboardInterrupt:
                stdout.write("\n")
                stdout.flush()
                continue
            except Exception as e:
                from traceback import print_exc
                print_exc()
                self._quit()
                continue

            line = line.split()
            if len(line) > 0 and line[0] not in self.ignore_list:
                if line[0] == "quit":
                    self._quit()
                    continue
                try:
                    m = getattr(self, line[0])
                    m(*line[1:])
                except AttributeError as e:
                    print "Attribute error:"
                    print e
                except TypeError as e:
                    print "Type error:"
                    print e

    def _quit(self):
        print "Pip-pip, old chap!"
        self.running = False

    def help(self):
        print "The following commands are supported:"
        for c in self.options:
            print "    " + c

    def usage(self):
        print "Enter 'help' for help or 'quit' to quit."

