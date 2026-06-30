#!/usr/bin/env python3
"""Backup the Supabase app_state row to a timestamped local file.
Free Supabase has no auto-backup, so we pull the single JSON blob and keep a rolling history.
Reads SUPABASE_URL / SUPABASE_ANON_KEY straight from index.html (one place to configure).
Run: python3 backup.py
"""
import json, re, sys, urllib.request, urllib.error
from pathlib import Path
from datetime import datetime

HERE = Path(__file__).parent
INDEX = HERE / "index.html"
BACKUP_DIR = HERE / "backups"
KEEP = 30  # ponytail: keep last 30 backups, delete older. Bump if you want a longer tail.
ROW_ID = "shared"

def read_creds():
    html = INDEX.read_text(encoding="utf-8")
    url = re.search(r"SUPABASE_URL\s*=\s*'([^']*)'", html)
    key = re.search(r"SUPABASE_ANON_KEY\s*=\s*'([^']*)'", html)
    return (url.group(1) if url else ""), (key.group(1) if key else "")

def main():
    url, key = read_creds()
    if not url or not key:
        sys.exit("ยังไม่ได้ตั้งค่า Supabase ใน index.html (SUPABASE_URL / SUPABASE_ANON_KEY ว่างอยู่) — backup ไม่ได้")

    api = f"{url}/rest/v1/app_state?id=eq.{ROW_ID}&select=data"
    req = urllib.request.Request(api, headers={"apikey": key, "Authorization": f"Bearer {key}"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            rows = json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"ดึงข้อมูลไม่สำเร็จ: HTTP {e.code} {e.read().decode(errors='replace')[:200]}")
    except urllib.error.URLError as e:
        sys.exit(f"ต่อ Supabase ไม่ได้: {e.reason}")

    if not rows:
        sys.exit("ไม่พบแถว app_state (ยังไม่มีข้อมูลในคลาวด์?) — ข้าม backup")

    data = rows[0]["data"]
    BACKUP_DIR.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d_%H%M")
    out = BACKUP_DIR / f"{ts}.json"
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    # prune oldest beyond KEEP
    files = sorted(BACKUP_DIR.glob("*.json"))
    for old in files[:-KEEP]:
        old.unlink()

    n = sum(len(t["subtasks"]) for s in data for t in s.get("tasks", [])) if isinstance(data, list) else "?"
    print(f"✓ backup → {out.relative_to(HERE)} ({out.stat().st_size} bytes, {len(data) if isinstance(data,list) else '?'} ไซต์, {n} งานย่อย)")

if __name__ == "__main__":
    main()
