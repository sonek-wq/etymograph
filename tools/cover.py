import os as _os
TOOLS=_os.path.dirname(_os.path.abspath(__file__)); ROOT=_os.path.dirname(TOOLS)
import json,sys,importlib.util,io,contextlib
spec=importlib.util.spec_from_file_location('a',_os.path.join(TOOLS,'audit2.py')); a=importlib.util.module_from_spec(spec); sys.argv=['x']
with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(a)
D=json.load(open(_os.path.join(ROOT,'etymo-data.json'))); P={p['id']:p for p in D['parts']}
out=[]
for w in D['words']:
    nm=a.fold(a.name(w)); ps=[P[x] for x in w['parts']]; b=a.place(nm,ps)
    cov=set()
    for c,s,e in b[1]:
        if c: cov.update(range(s,e))
    r=len(cov)/max(1,len(nm))
    roots=[p for p in ps if p['kind']=='root']
    if r<0.5 or not roots: out.append((round(r,2),w['id'],w['parts']))
out.sort()
for x in out: print(x)
print(len(out))
