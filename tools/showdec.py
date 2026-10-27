import os as _os
TOOLS=_os.path.dirname(_os.path.abspath(__file__)); ROOT=_os.path.dirname(TOOLS)
import json,sys,importlib.util
spec=importlib.util.spec_from_file_location('a',_os.path.join(TOOLS,'audit2.py')); a=importlib.util.module_from_spec(spec); sys.argv=['x']
import io,contextlib
with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(a)
D=json.load(open(_os.path.join(ROOT,'etymo-data.json'))); P={p['id']:p for p in D['parts']}; W={w['id']:w for w in D['words']}
for k in sys.argv[1:] if False else open(0).read().split():
    w=W[k]; ps=[P[x] for x in w['parts']]; b=a.place(a.fold(a.name(w)),ps)
    print(f"{k:13}", ' + '.join((c if c else '['+p.get('label',p['id'])+']')+'('+p['gloss']+')' for (c,s,e),p in zip(b[1],ps)), '｜', w['literal'])
