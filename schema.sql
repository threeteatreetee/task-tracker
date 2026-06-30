-- ตารางติดตามงาน — เก็บ state ทั้งหมดเป็น JSON ก้อนเดียว 1 แถว (no-login, ใช้ร่วมกัน)
create table if not exists app_state (
  id   text primary key,
  data jsonb not null,
  updated_at timestamptz default now()
);

-- เปิด Realtime ให้ทุกคนเห็นการเปลี่ยนแปลงสดๆ
alter publication supabase_realtime add table app_state;

-- RLS: เปิดให้ anon อ่าน/เขียนได้ (ลิงก์แชร์ในกลุ่มที่เชื่อใจกัน — ไม่มี login)
alter table app_state enable row level security;

create policy "anon read"   on app_state for select using (true);
create policy "anon insert" on app_state for insert with check (true);
create policy "anon update" on app_state for update using (true) with check (true);
