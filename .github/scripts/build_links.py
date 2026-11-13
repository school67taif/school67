#!/usr/bin/env python3
# يبني f/links.json تلقائياً من ملفات الموقع (يُشغَّل مع كل رفع)
import json, os, re, subprocess, sys, time

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "f", "links.json")
SELF = "f/الملفات والروابط.html"
AR = re.compile(r"[؀-ۿ]")
BIDI = re.compile(r"[‎‏⁦-⁩‪-‮]")
SKIP_DIRS = {".git", ".github", "lib", "img", "sig", "fonts", "ghiyab", "rep48", "nafs48"}
SUFFIX = re.compile(r"\s*[·\-–—|]\s*(الابتدائية\s*(السابعة\s*والستون|67)[^·\-–—|]*)$")
PREFIX = re.compile(r"^الابتدائية السابعة والستون\s*[–\-]\s*الطائف\s*·\s*")


def title_of(path):
    try:
        with open(path, "rb") as fh:
            head = fh.read(400000).decode("utf8", "ignore")
    except Exception:
        return None, ""
    m = re.search(r"<title>([^<]*)</title>", head)
    return (m.group(1).strip() if m else None), head


def clean(name):
    name = BIDI.sub("", name).strip()
    name = PREFIX.sub("", name)
    for _ in range(2):
        name = SUFFIX.sub("", name).strip()
    return re.sub(r"\s+", " ", name)


def is_redirect(head, size):
    return size < 4000 and ("http-equiv=\"refresh\"" in head or "location.replace" in head)


CATS = ["النظام والأدلة", "المنصات", "السجلات", "الملفات", "التقارير والشواهد",
        "الخطط والمبادرات والمشاريع", "النماذج والاستمارات", "الاجتماعات والورش", "مواد تعليمية وأخرى"]


def norm(x):
    x = clean(BIDI.sub("", x)).replace("_", " ")
    x = re.sub(r"\s*[·\-–—]\s*الابتدائية\s*(السابعة\s*والستون|67)", "", x)
    x = re.sub(r"هـ\b|هـ$", "", x)
    return re.sub(r"\s+", " ", x).strip()


def category(n):
    rules = [
        ("النظام والأدلة", r"^(النظام|دليل|مكتبة|داشبورد|اللوحة|لوحة|صلاحي)"),
        ("المنصات", r"^منصة"),
        ("السجلات", r"^(سجل|كشوف|السجلات)"),
        ("الملفات", r"^(ملف|ملفات|حقيبة|برامج|البروشورات)"),
        ("التقارير والشواهد", r"^(تقرير|تقارير|إفادة|شواهد|متابعة|الشواهد|ملخص|عرض|نتائج)"),
        ("الخطط والمبادرات والمشاريع", r"^(خطة|الخطة|مبادرة|مشروع|برنامج|بطاقة|بطاقات|راية)"),
        ("النماذج والاستمارات", r"^(استمارة|نماذج|نموذج|أداة|توقيع|قياس|جدول|إعلان|ملصق)"),
        ("الاجتماعات والورش", r"^(اجتماع|ورشة|لقاء)"),
    ]
    for c, rx in rules:
        if re.search(rx, n):
            return c
    return "مواد تعليمية وأخرى"


def mtime(rel):
    try:
        out = subprocess.run(["git", "log", "-1", "--format=%ct", "--", rel], cwd=ROOT,
                             capture_output=True, text=True, timeout=30).stdout.strip()
        if out:
            return int(out)
    except Exception:
        pass
    return int(os.path.getmtime(os.path.join(ROOT, rel)))


def candidates():
    for dp, dns, fns in os.walk(ROOT):
        rel_dir = os.path.relpath(dp, ROOT).replace(os.sep, "/")
        dns[:] = [d for d in dns if d not in SKIP_DIRS and not d.startswith(".")]
        depth = 0 if rel_dir == "." else rel_dir.count("/") + 1
        has_index = "index.html" in fns
        for fn in fns:
            rel = fn if rel_dir == "." else rel_dir + "/" + fn
            ext = fn.rsplit(".", 1)[-1].lower() if "." in fn else ""
            if ext not in ("html", "pdf") or rel == SELF or fn == "_t.html":
                continue
            if depth >= 1 and has_index and fn != "index.html" and rel_dir not in ("f", "dl"):
                continue  # ملفات داخل مجلد له صفحة رئيسية
            if depth >= 2 and rel_dir.split("/")[1] == "بروشور" and fn != "index.html":
                continue
            if fn != "index.html" and not AR.search(fn) and depth > 0:
                continue
            yield rel, ext


def main():
    items = {}
    pri = lambda rel: (0 if rel.startswith("f/") else 1 if rel == "index.html" else 2 if not rel.startswith("dl/") else 3)
    pdfs = []
    for rel, ext in candidates():
        full = os.path.join(ROOT, rel)
        size = os.path.getsize(full)
        stem = BIDI.sub("", os.path.basename(rel).rsplit(".", 1)[0]).strip()
        if ext == "html":
            t, head = title_of(full)
            if is_redirect(head, size):
                continue
            name = clean(t or stem)
            if "'+" in name or not name:
                name = clean(stem)
            if os.path.basename(rel) == "index.html" and rel != "index.html" and not t:
                continue
        else:
            name = clean(stem)
            pdfs.append((rel, name))
            continue
        key = name
        cur = items.get(key)
        if cur:
            a = (pri(cur["p"]), 0 if norm(cur["s"]) == norm(name) else 1, -cur["z"])
            b = (pri(rel), 0 if norm(stem) == norm(name) else 1, -size)
            if a <= b:
                continue
        items[key] = {"n": name, "p": rel, "t": "html", "c": category(name), "u": mtime(rel), "s": stem, "z": size}
    by_norm = {}
    for k, v in items.items():
        by_norm.setdefault(norm(v["n"]), k)
        by_norm.setdefault(norm(v["s"]), k)
    pdfs.sort(key=lambda x: (x[0].count("/"), x[0]))
    seen_pdf = set()
    for rel, name in pdfs:
        stem = BIDI.sub("", os.path.basename(rel).rsplit(".", 1)[0]).strip()
        ev = re.split(r"\s+—\s+تقارير وشواهد", name)
        if len(ev) > 1:  # تقارير وشواهد جاهزة للاعتماد تُلحق بملفها
            k = by_norm.get(norm(ev[0]))
            if k:
                items[k].setdefault("x", []).append({"n": "تقارير وشواهد " + ev[1].strip() + " PDF", "p": rel})
                continue
            name = clean(ev[0]) + " — تقارير وشواهد" + ev[1]
        k = by_norm.get(norm(stem)) or by_norm.get(norm(name))
        if k and "pdf" not in items[k] and items[k]["t"] == "html":
            items[k]["pdf"] = rel
            continue
        if norm(name) in seen_pdf:
            continue
        seen_pdf.add(norm(name))
        items[name + " (PDF)" if name in items else name] = {"n": name, "p": rel, "t": "pdf", "c": category(name), "u": mtime(rel)}
    lst = sorted(items.values(), key=lambda x: (CATS.index(x["c"]), x["n"]))
    for x in lst:
        x.pop("s", None); x.pop("z", None)
    data = {"updated": int(time.time()), "count": len(lst), "items": lst}
    old = None
    if os.path.exists(OUT):
        try:
            old = json.load(open(OUT, encoding="utf8"))
        except Exception:
            pass
    if old and old.get("items") == lst:
        print("links.json: لا تغيير (%d)" % len(lst))
        return
    with open(OUT, "w", encoding="utf8") as fh:
        json.dump(data, fh, ensure_ascii=False, separators=(",", ":"))
    print("links.json: %d رابط" % len(lst))


if __name__ == "__main__":
    main()
