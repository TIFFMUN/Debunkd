import { createClient } from "https://cdn.jsdelivr.net/npm/@supabase/supabase-js/+esm";

const SUPABASE_URL = "https://ikdqppngzxmmklmwhwsn.supabase.co";
const SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlrZHFwcG5nenhtbWtsbXdod3NuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDE0OTUyNzQsImV4cCI6MjA1NzA3MTI3NH0.fZXWbU9i6gEGElDP69BJzna8gJGoMp9qQfnTLuWblxs";

export const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
