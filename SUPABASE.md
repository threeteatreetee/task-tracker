# ทำให้ใช้ร่วมกัน online (Supabase)

`index.html` ทำงานได้ 2 โหมด:
- **เว้น config ว่าง** → เก็บใน localStorage เครื่องเดียว (โหมดปัจจุบัน)
- **เติม config Supabase** → ทุกคนเห็นงานกองเดียวกัน + เด้งสดแบบ realtime, ไม่ต้อง login

> เก็บข้อมูลเป็น JSON ก้อนเดียว 1 แถว = **last-write-wins** ถ้า 2 คนกดแก้พร้อมกันเป๊ะๆ คนเซฟทีหลังทับ เหมาะกับเพื่อน/ทีมไม่กี่คน

---

## 1. สมัคร Supabase + สร้าง project (ฟรี)
1. ไป https://supabase.com → Sign in (ใช้ GitHub ได้) → **New project**
2. ตั้งชื่อ + รหัส database (จำไว้) → เลือก region **Southeast Asia (Singapore)** → Create
3. รอ ~2 นาทีให้ project พร้อม

## 2. สร้างตาราง — รัน SQL
Supabase → เมนูซ้าย **SQL Editor** → New query → วาง `schema.sql` (ในโฟลเดอร์นี้) ทั้งก้อน → **Run**

ตารางนี้เปิดให้ใครก็อ่าน/เขียนได้ (no-login) — เหมาะกับลิงก์แชร์ในกลุ่มที่เชื่อใจกัน

## 3. เอา URL + key มาใส่ในหน้าเว็บ
Supabase → **Project Settings** (เฟือง) → **API** → ก๊อป:
- **Project URL**
- **anon public** key (อันยาวๆ ใต้ "Project API keys" — **ห้ามใช้ `service_role`**)

เปิด `index.html` แก้ 2 บรรทัดบนสุดของ `<script>`:
```js
const SUPABASE_URL = 'https://xxxx.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGc...';
```

เปิดไฟล์ทดสอบ — เพิ่มงานในเครื่องนึง อีกเครื่องควรเห็นภายในไม่กี่วินาที

## 4. อัปขึ้น host (เลือกอย่างใดอย่างหนึ่ง)
- **Netlify (ลากวาง):** https://app.netlify.com/drop → ลากโฟลเดอร์ `task-tracker` ทั้งโฟลเดอร์ → ได้ URL ทันที
- **GitHub Pages:** push โฟลเดอร์ขึ้น repo → Settings > Pages > Deploy from branch (เหมือนที่ทำกับ eyer-3d)

แชร์ URL ให้เพื่อน — เปิดได้ทุกเครื่องที่มีเบราว์เซอร์

---

## หมายเหตุความปลอดภัย
anon key ฝังในหน้าเว็บ = ใครมี URL ก็แก้ข้อมูลได้ ถ้าเริ่มกังวล (ข้อมูลสำคัญ/คนนอกหลุดเข้ามา) ค่อยเพิ่ม Supabase Auth (magic-link) ทีหลัง — โครงปัจจุบันไม่ต้องรื้อ
