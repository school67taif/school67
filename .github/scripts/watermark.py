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

# أي صفحة جديدة بدون قفل: يُضاف لها القفل والعلامة المائية تلقائياً
SKIP = {"f/الملفات والروابط.html", "f/_t.html", "index.html"}
try:
    src = open("f/إعلان لقاء HPV.html", encoding="utf8").read()
    a = src.find('<script id="s67guard">'); b = src.find('</script>', a) + 9
    GUARD = src[a:b] if a >= 0 else None
except Exception:
    GUARD = None
added = 0
if GUARD and "s67wm" in GUARD:
    for f in glob.glob("**/*.html", recursive=True):
        if f in SKIP or f.startswith("dl/النظام المتكامل") or f.startswith(".github"):
            continue
        s = open(f, encoding="utf8", errors="ignore").read()
        if "s67guard" in s or len(s) < 4000 or 'http-equiv="refresh"' in s or "location.replace(" in s[:3000]:
            continue
        k = s.lower().rfind("</body>")
        s = (s[:k] + GUARD + s[k:]) if k >= 0 else s + GUARD
        open(f, "w", encoding="utf8").write(s); added += 1
print("guard added", added)

# تحديث تلقائي: إذا كان المتصفح يعرض نسخة قديمة من الصفحة يجلب الجديدة ويعيد التحميل مرة واحدة
FRESH = '<script id="s67fresh">(function(){try{var u=location.href.split("#")[0];if(!/^https?:/.test(u)||sessionStorage.getItem("s67f:"+u))return;sessionStorage.setItem("s67f:"+u,"1");Promise.all([fetch(u,{method:"HEAD",cache:"force-cache"}),fetch(u,{method:"HEAD",cache:"reload"})]).then(function(r){var a=r[0].headers.get("etag")||r[0].headers.get("last-modified"),b=r[1].headers.get("etag")||r[1].headers.get("last-modified");if(a&&b&&a!==b)location.reload()}).catch(function(){})}catch(e){}})();</script>'
nf = 0
for f in glob.glob("**/*.html", recursive=True):
    if f.startswith(".github"):
        continue
    s = open(f, encoding="utf8", errors="ignore").read()
    if "s67fresh" in s or "s67guard" not in s:
        continue
    i = s.find('<script id="s67guard">')
    s = s[:i] + FRESH + s[i:]
    open(f, "w", encoding="utf8").write(s); nf += 1
print("fresh added", nf)
