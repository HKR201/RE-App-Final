import flet as ft
import requests
import traceback # Error ရှာဖို့အတွက်

# --- CONFIGURATION ---
SUPABASE_URL = "https://btwbbjijrbyxbjlhtpqf.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJ0d2JiamlqcmJ5eGJqbGh0cHFmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzMzODIwNjEsImV4cCI6MjA4ODk1ODA2MX0.jkVvPfaEvhhWDg7zTdjKnll5gDqeyNBy3Eli4cxmbhQ"
HEADERS = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"}

def main(page: ft.Page):
    try:
        page.title = "RE Dashboard"
        page.theme_mode = "light"
        
        # UI version Compatibility Fix
        def login_view():
            u = ft.TextField(label="Username", border_radius=10)
            p = ft.TextField(label="Password", password=True, can_reveal_password=True)
            
            def do_login(e):
                if u.value == "admin" and p.value == "1478963":
                    page.clean()
                    page.add(ft.Text("Login Success! Loading Data..."))
                    # Data fetch logic here...
                else:
                    page.snack_bar = ft.SnackBar(ft.Text("Login Failed"))
                    page.snack_bar.open = True
                    page.update()

            return ft.Column([
                ft.Icon(name="home_work", size=50, color="blue"),
                ft.Text("RE HUB", size=25, weight="bold"),
                u, p,
                ft.ElevatedButton("Login", on_click=do_login, width=300)
            ], horizontal_alignment="center")

        page.add(login_view())
        page.update()

    except Exception as e:
        # တကယ်လို့ App crash ရင် ဘာကြောင့်လဲဆိုတာ Screen ပေါ်မှာ ပြပေးမယ့် debug logic
        error_msg = traceback.format_exc()
        page.add(ft.Text(f"Critical Error:\n{error_msg}", color="red", size=12))
        page.update()

# Native APK အတွက် ft.app(target=main) ကိုပဲ သုံးရပါမယ်
if __name__ == "__main__":
    ft.app(target=main)
    
