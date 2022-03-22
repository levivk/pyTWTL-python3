'''
An interface for code by Cristian Ioan Vasile <cvasile@bu.edu> that translates a TWTL expression into a DFA.
This interface was built so that the TWTL translation can be run as a standalone program with a packaged Python 2.7.

Author: Levi Vande Kamp
Date: March 2022
'''
# Create a custom importer so that a few unused imports can be excluded from the package but not cause import errors
import __builtin__
from types import ModuleType
class DummyModule(ModuleType):
    def __getattr__(self, key):
        return None
    __all__ = []

class PkgResourcesDummy(ModuleType):
    def resource_exists(self, foo, bar):
        return True
    def resource_filename(self, foo, bar):
        return None

# Exclude some unused things. Many more could be added here to further decrease size, but this is good enough.
ignore_modules = [
    'lomap.algorithms.optimal_run',
    'lomap.algorithms.multi_agent_optimal_run',
    'lomap.algorithms.robust_multi_agent_optimal_run'
]

# Replacement import function for ignoring problematic/unneeded imports
def tryimport(name, globals={}, locals={}, fromlist=[], level=-1):
    # pkg_resources is unused and causes some problems with pyinstaller
    if name == 'pkg_resources':
        return PkgResourcesDummy(name)
    elif name in ignore_modules:
        return DummyModule(name)
    else:
        return realimport(name, globals, locals, fromlist, level)


realimport = __builtin__.__import__
__builtin__.__import__ = tryimport

# Continue as normal
import argparse
import yaml
# import networkx as nx
# from StringIO import StringIO

import twtl
from dfa import DFAType

parser = argparse.ArgumentParser(description=
    "Converts a TWTL formula into an FSA. It can return both a normal FSA or " +
    "the automaton corresponding to the relaxed infinity version of the " +
    "specification.\n\n" +
    "This program prints to standard output a PyYAML serialized dictionary containing: (a) the alphabet; " +
    "(b) the normal automaton (if requested); (c) the infinity version automaton "+
    "(if requested); and (d) the bounds of the TWTL formula (if requested).\n\n" +
    "This is an interface for code by Cristian Ioan Vasile <cvasile@bu.edu> that translates a TWTL expression into a DFA. " +
    "This interface was built so that the TWTL translation can be run as a standalone program with a packaged Python 2.7.")

parser.add_argument('formula', type=str, help='The TWTL formula')
parser.add_argument('--kind', type=str, choices=['normal', 'infinity', 'both'], default='both',
        help="'normal': Returns only the normal version.\n"
            +"'infinity': Returns only the relaxed version.\n"
            +"'both': Returns both automata versions.")
parser.add_argument('--norm', action='store_true', help='Compute the bounds of the TWTL Formula')
parser.add_argument('--dont-optimize', dest='optimize', action='store_false', 
        help="Don't optimize annotation data. Note that the synthesis algorithm assumes " +
            "an optimized automaton, while computing temporal relaxations is performed using " +
            "an unoptimized automaton.")

args = parser.parse_args()

kind_dict = {
    'normal': DFAType.Normal,
    'infinity': DFAType.Infinity,
    'both': 'both'
}

dfa_kind = kind_dict[args.kind]

output = twtl.translate(args.formula, kind=dfa_kind, norm=args.norm, optimize=args.optimize)

print(yaml.dump(output))
