# علامة مائية باسم مديرة المدرسة في كل ملف لغير المديرة
import glob,re,sys
CSS="#s67wm{position:fixed;inset:0;pointer-events:none;z-index:2147483640;overflow:hidden;display:none}html.s67lock #s67wm{display:block}#s67wm div{position:absolute;white-space:nowrap;text-align:center;line-height:1.7;transform:rotate(-28deg);color:rgba(102,0,51,.11);font:700 20px 'Noto Kufi Arabic',Tahoma,sans-serif}@media print{#s67wm{display:none!important}}"
JS='if(!d.getElementById("s67wm")){var w=d.createElement("div");w.id="s67wm";w.setAttribute("aria-hidden","true");var hh="";for(var y=-1;y<14;y++)for(var x=-1;x<7;x++)hh+=\'<div style="top:\'+(y*140)+\'px;left:\'+(x*300+(y%2)*150)+\'px">ناديه عوض الصخيري<br>الابتدائية السابعة والستون</div>\';w.innerHTML=hh;d.body.appendChild(w)}'
def patch_guard(g):
    if "s67wm" in g: return g
    a='(d.head||de).appendChild(st);'; b='function init(){scan();'
    assert a in g and b in g
    g=g.replace(a,'st.textContent+="'+CSS+'";'+a,1)
    g=g.replace(b,b+JS,1)
    return g
canon=None
import os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..",".."))
files=[f for f in glob.glob("**/*.html",recursive=True)]
n=0
for f in files:
    s=open(f,encoding="utf8").read()
    i=s.find('<script id="s67guard">')
    if i<0: continue
    j=s.find('</script>',i)
    g=s[i:j]; g2=patch_guard(g)
    if f=="f/إعلان لقاء HPV.html": canon=g2
    if g2!=g: s=s[:i]+g2+s[j:]; open(f,"w",encoding="utf8").write(s); n+=1
print("patched",n)
