-- ล็อก RLS ให้เฉพาะคนที่ login เท่านั้นเข้าถึง app_state ได้ (รันหลังจาก schema.sql)
-- รันใน Supabase > SQL Editor

drop policy if exists "anon read"   on app_state;
drop policy if exists "anon insert" on app_state;
drop policy if exists "anon update" on app_state;

create policy "auth read"   on app_state for select to authenticated using (true);
create policy "auth insert" on app_state for insert to authenticated with check (true);
create policy "auth update" on app_state for update to authenticated using (true) with check (true);
