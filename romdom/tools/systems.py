import json
import itertools
import difflib
from collections import Counter
from ..sites import *


def unique_systems(save_file='systems.json'):
    systems = []
    for cls in BaseSite.derived():
        site = cls()
        systems.extend(site.get_systems())
    cnt = list(Counter(systems))
    if save_file:
        json.dump(cnt, open(save_file, 'w'))
    return cnt


def all_systems():
    systems = {}
    for cls in BaseSite.derived():
        name = cls.__name__
        site = cls()
        systems[name] = list(site.get_systems())
    return systems


def print_all_systems():
    systems = all_systems()
    systems_list = []
    for s in systems:
        systems_list.append([s] + sorted(systems[s]))

    lengths = [max(map(len, s)) for s in systems_list]
    for row in itertools.izip_longest(*systems_list, fillvalue=''):
        for i, r in enumerate(row):
            print r.center(lengths[i]),
        print


def string_similarity(a, b):
    return difflib.SequenceMatcher(a=a.lower(), b=b.lower()).ratio()


def group_similar_systems():
    systems = all_systems().values()
    groups = []
    comb = itertools.combinations(systems, 2)
    for c in comb:
        for p in itertools.product(*c):
            sim = string_similarity(p[0], p[1])
            if sim > .6:
                #print '%6.2f %s' % (sim * 100, str(p))
                p = set(p)
                for g in groups:
                    if g & p:
                        groups.remove(g)
                        g |= p
                        groups.append(g)
                        break
                else:
                    groups.append(set(p))
            else:
                for elem in p:
                    for g in groups:
                        if elem in g:
                            break
                    else:
                        groups.append(set((elem,)))
    for g in groups:
        print g
        

if __name__ == '__main__':
    #unique_systems()
    #group_similar_systems()
    print_all_systems()
