from framework.brains.colorize.console import ColorizeConsole
from androguard.core.analysis import analysis
from androguard.decompiler.dad import decompile
from datetime import datetime
from blessings import Terminal
console = ColorizeConsole()
t = Terminal()


class BowserEnum(object):

    values = {

        "android.content.Intent": [

            "parseUri",
            "setSelector"

        ],

        "android.webkit.WebView": [

            "addJavascriptInterface",
            "loadUrl",
            "loadData"
        ]

    }


class Bowser(object):

    name = "bowser"

    def __init__(self, vm, vm_type):
        # The vm_type argument is always determined through the loader
        super(Bowser, self).__init__()
        self.vm = vm
        self.vm_type = vm_type
        self.enum = BowserEnum()

    def run(self):

        """
        Search for Web Browser API usage within target class and methods
        """

        if self.vm_type == "apks":
            # Get the DVM analysis object from Androguard
            _x = analysis.uVMAnalysis(self.vm.get_vm())
            _vm = self.vm.get_vm()
            _structure = list()

            if _x:
                print(t.green("[{0}] ".format(datetime.now()) + t.yellow("Performing surgery ...")))
                for a, b in self.enum.values.items():
                    for c in b:
                        paths = _x.get_tainted_packages().search_methods("{0}".format(a), "{0}".format(c), ".")
                        if paths:
                            for p in paths:
                                for method in self.vm.get_methods():
                                    if method.get_name() == p.get_src(_vm.get_class_manager())[1]:
                                        if method.get_class_name() == p.get_src(_vm.get_class_manager())[0]:
                                            # Start decompilation process for each method
                                            mx = _x.get_method(method)
                                            d = decompile.DvMethod(mx)
                                            d.process()
                                            _structure.append((c, method, d))
            # Iterate through the generated methods and
            # create a unique set
            methods = [s[0] for s in _structure]
            methods_set = set(methods)

            for m in methods_set:
                print(t.green("[{0}] ".format(datetime.now()) +
                              t.yellow("Available bowser method: ") + "{0}".format(m)))

            print(t.green("[{0}] ".format(datetime.now()) + t.yellow("Enter \'back\' to exit")))
            print(t.green("[{0}] ".format(datetime.now()) + t.yellow("Enter \'list\' to show available methods")))

            while True:
                # Selected target method
                method = raw_input(t.green("[{0}] ".format(datetime.now()) + t.yellow("Enter method selection: ")))

                for s in _structure:
                    if method == s[0]:
                        print(t.green("[{0}] ".format(datetime.now()) +
                                      t.yellow("Found: ") +
                                      "{0}".format(s[0])))
                        print(t.green("[{0}] ".format(datetime.now()) +
                                      t.yellow("Class: ") +
                                      "{0}".format(s[1].get_class_name())))
                        print(t.green("[{0}] ".format(datetime.now()) +
                                      t.yellow("Method: ") +
                                      "{0}".format(s[1].get_name())))

                        print("".join([s[1].get_class_name(), "->", s[1].get_name(),
                                       s[1].get_descriptor(), s[1].get_access_flags_string()]))

                        print(s[1].show())
                        console.colorize_decompiled_method(str(s[2].get_source()))

                if method == "back":
                    break
                elif method == "list":
                    for m in methods_set:
                        print(t.green("[{0}] ".format(datetime.now()) +
                              t.yellow("Available bowser method: ") + "{0}".format(m)))

        elif self.vm_type == "dex":

            _x = analysis.uVMAnalysis(self.vm)
            _vm = self.vm
            _structure = list()

            if _x:
                print(t.green("[{0}] ".format(datetime.now()) + t.yellow("Performing surgery ...")))
                for a, b in self.enum.values.items():
                    for c in b:
                        paths = _x.get_tainted_packages().search_methods("{0}".format(a), "{0}".format(c), ".")
                        if paths:
                            for p in paths:
                                for method in self.vm.get_methods():
                                    if method.get_name() == p.get_src(_vm.get_class_manager())[1]:
                                        if method.get_class_name() == p.get_src(_vm.get_class_manager())[0]:
                                            # Start decompilation process for each method
                                            mx = _x.get_method(method)
                                            d = decompile.DvMethod(mx)
                                            d.process()
                                            _structure.append((c, method, d))
            # Iterate through the generated methods and
            # create a unique set
            methods = [s[0] for s in _structure]
            methods_set = set(methods)

            for m in methods_set:
                print(t.green("[{0}] ".format(datetime.now()) +
                              t.yellow("Available bowser method: ") + "{0}".format(m)))

            print(t.green("[{0}] ".format(datetime.now()) + t.yellow("Enter \'back\' to exit")))
            print(t.green("[{0}] ".format(datetime.now()) + t.yellow("Enter \'list\' to show available methods")))

            while True:
                # Selected target method
                method = raw_input(t.green("[{0}] ".format(datetime.now()) + t.yellow("Enter method selection: ")))

                for s in _structure:
                    if method == s[0]:
                        print(t.green("[{0}] ".format(datetime.now()) +
                                      t.yellow("Found: ") +
                                      "{0}".format(s[0])))
                        print(t.green("[{0}] ".format(datetime.now()) +
                                      t.yellow("Class: ") +
                                      "{0}".format(s[1].get_class_name())))
                        print(t.green("[{0}] ".format(datetime.now()) +
                                      t.yellow("Method: ") +
                                      "{0}".format(s[1].get_name())))
                        print(s[1].show())
                        console.colorize_decompiled_method(str(s[2].get_source()))

                if method == "back":
                    break
                elif method == "list":
                    for m in methods_set:
                        print(t.green("[{0}] ".format(datetime.now()) +
                              t.yellow("Available bowser method: ") + "{0}".format(m)))
