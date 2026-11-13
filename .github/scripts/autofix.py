# يضيف اعتماد المديرة والختم وزر الرجوع لأي صفحة جديدة ناقصة
import glob,os,re
D=os.path.dirname(__file__)
A=open(os.path.join(D,'appr.html'),encoding='utf-8').read().strip()
BK=open(os.path.join(D,'back.html'),encoding='utf-8').read().strip()
NS=open(os.path.join(D,'nosave.html'),encoding='utf-8').read().strip()
SR=open(os.path.join(D,'srch.html'),encoding='utf-8').read().strip()
m=re.search(r'data:image/[a-z]+;base64,([A-Za-z0-9+/]{100})',A); P=m.group(1) if m else None
def redirect(t): return len(t)<4000 and re.search(r'http-equiv=["\']?refresh|location\.replace',t,re.I)
n=0
for f in glob.glob('f/**/*.html',recursive=True):
    t=open(f,encoding='utf-8',errors='surrogateescape').read();o=t
    if redirect(t): continue
    top=os.path.dirname(f)=='f' and not os.path.basename(f).startswith('_')
    if top and 's67appr' not in t and 's67sigs' not in t and not (P and P in t):
        c=[x for x in (t.rfind(k) for k in ('<script id="s67guard">','<script id="s67archive">','<script id="s67photo">','<script id="s67back">')) if x>0]
        i=min(c) if c else t.rfind('</body>'); t=t[:i]+A+t[i:] if i>=0 else t+A
    if 'id="s67back"' not in t:
        i=t.rfind('</body>'); t=t[:i]+BK+t[i:] if i>=0 else t+BK
    if 'id="s67nosave"' not in t:
        i=t.rfind('</body>'); t=t[:i]+NS+t[i:] if i>=0 else t+NS
    if 'id="s67srch"' not in t:
        i=t.rfind('</body>'); t=t[:i]+SR+t[i:] if i>=0 else t+SR
    if t!=o: open(f,'w',encoding='utf-8',errors='surrogateescape').write(t); n+=1; print('fixed',f)
print('autofix',n)
