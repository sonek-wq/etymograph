import os as _os
TOOLS=_os.path.dirname(_os.path.abspath(__file__)); ROOT=_os.path.dirname(TOOLS)
import json, unicodedata, re, sys, itertools
D = json.load(open(sys.argv[1] if len(sys.argv)>1 else _os.path.join(ROOT,'etymo-data.json')))
P = {p['id']: p for p in D['parts']}
def fold(x): return ''.join(c for c in unicodedata.normalize('NFKD', x.lower()) if not unicodedata.combining(c))
def name(w): return w.get('label') or re.sub(r'\(\d+\)$', '', w['id'])
def cands(p):
    lab = p.get('label', p['id'])
    cs = list(dict.fromkeys([x.strip() for x in lab.split('/')] + [p['id']] + (p.get('forms') or [])))
    out = []
    for c in cs:
        b = re.sub(r'\(.*?\)', '', fold(c)).replace('-', '')
        if b and (c, b) not in out: out.append((c, b))
    return out
def place(word, ps):
    n = len(ps); opts = []
    for i, p in enumerate(ps):
        o = [(None, None, None)]
        for c, b in cands(p):
            starts = [m.start() for m in re.finditer('(?=' + re.escape(b) + ')', word)]
            if p['kind'] == 'prefix' and i == 0: starts = [s for s in starts if s == 0]
            if p['kind'] == 'suffix' and i == n-1: starts = [s for s in starts if s + len(b) == len(word)]
            o += [(c, s, s + len(b)) for s in starts]
        opts.append(o)
    best = None
    for combo in itertools.product(*opts):
        miss = ov = cov = 0; prev = 0; ok = True; seen = set()
        for c, s, e in combo:
            if c is None: miss += 1; continue
            if s < prev - 1 or s < 0: ok = False; break
            ov += max(0, prev - s)
            prev = max(prev, e); cov += e - s
        if not ok: continue
        cost = (miss, ov, -cov)
        if best is None or cost < best[0]: best = (cost, combo)
    return best
if __name__ == '__main__':
    probs = []
    for w in D['words']:
        word = fold(name(w)); ps = [P[x] for x in w['parts']]
        b = place(word, ps)
        if b is None or b[0][0] or b[0][1]:
            probs.append((w['id'], w['parts'], b and b[0][:2], b and [c for c, s, e in b[1]]))
    for p in probs: print(p)
    print(len(probs))
