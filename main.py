import flet as ft
import requests
import traceback

# --- CONFIGURATION ---
SUPABASE_URL = "https://btwbbjijrbyxbjlhtpqf.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJ0d2JiamlqcmJ5eGJqbGh0cHFmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzMzODIwNjEsImV4cCI6MjA4ODk1ODA2MX0.jkVvPfaEvhhWDg7zTdjKnll5gDqeyNBy3Eli4cxmbhQ"
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# --- DATABASE API ENGINE ---
class API:
    @staticmethod
    def fetch(table):
        try:
            res = requests.get(f"{SUPABASE_URL}/rest/v1/{table}?is_deleted=eq.0&order=id.desc", headers=HEADERS, timeout=10)
            return res.json() if res.status_code == 200 else []
        except: return []

    @staticmethod
    def insert(table, data):
        try:
            res = requests.post(f"{SUPABASE_URL}/rest/v1/{table}", headers=HEADERS, json=data, timeout=10)
            return res.status_code in [200, 201]
        except: return False

    @staticmethod
    def soft_delete(table, record_id):
        try:
            res = requests.patch(f"{SUPABASE_URL}/rest/v1/{table}?id=eq.{record_id}", headers=HEADERS, json={"is_deleted": 1}, timeout=10)
            return res.status_code in [200, 204]
        except: return False

# --- MAIN APP UI ---
def main(page: ft.Page):
    try:
        page.title = "RE Dashboard Pro"
        page.theme_mode = "light"
        page.bgcolor = "#F4F7F6"
        page.padding = 0

        def show_snack(text, color="green"):
            page.snack_bar = ft.SnackBar(ft.Text(text, weight="bold"), bgcolor=color)
            page.snack_bar.open = True
            page.update()

        # Custom Router to avoid Flet Version Warnings
        def navigate(route):
            page.route = route
            route_change(None)

        # 1. LOGIN VIEW
        def login_view():
            u = ft.TextField(label="Username", border_radius=12, prefix_icon="person")
            p = ft.TextField(label="Password", password=True, can_reveal_password=True, border_radius=12, prefix_icon="lock")
            
            def do_login(e):
                if u.value == "admin" and p.value == "1478963":
                    page.client_storage.set("auth", True)
                    navigate("/main")
                else: show_snack("အချက်အလက် မှားယွင်းနေပါသည်။", "red")

            return ft.View(route="/login", controls=[
                ft.Container(expand=True, padding=30, alignment="center", content=ft.Column([
                    ft.Icon(name="home_work", size=80, color="#1565C0"), 
                    ft.Text("Vibe ERP Mobile", size=24, weight="bold", color="#0D47A1"),
                    ft.Divider(height=30, color="transparent"), u, p, ft.Container(height=10),
                    ft.ElevatedButton(text="Login", on_click=do_login, width=float('inf'), height=50, bgcolor="#1565C0", color="white")
                ], horizontal_alignment="center", alignment="center"))
            ])

        # 2. MAIN DASHBOARD VIEW
        def main_dashboard_view():
            def get_props_tab():
                items = API.fetch("apk_properties")
                lv = ft.ListView(expand=True, spacing=15, padding=15)
                if not items: lv.controls.append(ft.Container(content=ft.Text("ဒေတာမရှိသေးပါ။", color="grey"), padding=20, alignment="center"))
                for i in items:
                    lv.controls.append(ft.Container(bgcolor="white", padding=15, border_radius=15, shadow=ft.BoxShadow(blur_radius=10, color="black12"), content=ft.Column([
                        ft.Row([ft.Container(content=ft.Text(i.get('status', 'Available'), size=10, weight="bold", color="white"), bgcolor="green" if i.get('status') != 'Sold' else "red", padding=5, border_radius=5), ft.IconButton(icon="delete", icon_color="red", on_click=lambda e, rid=i['id']: delete_record("apk_properties", rid))], alignment="spaceBetween"),
                        ft.Text(i.get('title', 'No Title'), weight="bold", size=18, max_lines=1), ft.Text(f"{i.get('asking_price', 0):,.0f} သိန်း", color="#1565C0", size=22, weight="bold"),
                        ft.Text(f"📍 {i.get('location', '')} | 👤 {i.get('owner_name', '')}", size=12, color="grey")
                    ])))
                return ft.Column([ft.Container(bgcolor="#1565C0", padding=15, content=ft.Row([ft.Text("Properties", size=20, weight="bold", color="white"), ft.IconButton(icon="add_circle", icon_color="white", on_click=lambda _: navigate("/add_prop"))], alignment="spaceBetween")), lv], expand=True, spacing=0)

            def get_buyers_tab():
                items = API.fetch("apk_buyers")
                lv = ft.ListView(expand=True, spacing=10, padding=15)
                for i in items: lv.controls.append(ft.ListTile(leading=ft.Icon(name="person", color="purple"), title=ft.Text(f"{i.get('name')} - {i.get('budget')} သိန်း", weight="bold"), subtitle=ft.Text(f"📞 {i.get('phone')} | 📍 {i.get('location')}"), bgcolor="white"))
                return ft.Column([ft.Container(bgcolor="purple", padding=15, content=ft.Row([ft.Text("Buyers", size=20, weight="bold", color="white"), ft.IconButton(icon="add", icon_color="white")], alignment="spaceBetween")), lv], expand=True, spacing=0)

            def get_owners_tab():
                items = API.fetch("apk_owners")
                lv = ft.ListView(expand=True, spacing=10, padding=15)
                for i in items: lv.controls.append(ft.ListTile(leading=ft.Icon(name="real_estate_agent", color="orange"), title=ft.Text(i.get('name'), weight="bold"), subtitle=ft.Text(f"📞 {i.get('phone', 'No Phone')}"), bgcolor="white"))
                return ft.Column([ft.Container(bgcolor="#E65100", padding=15, content=ft.Text("Owners", size=20, weight="bold", color="white")), lv], expand=True, spacing=0)

            def delete_record(table, rid):
                if API.soft_delete(table, rid): show_snack("ဖျက်သိမ်းပြီးပါပြီ"); navigate("/main")
                else: show_snack("Network Error", "red")

            content_area = ft.Container(content=get_props_tab(), expand=True)

            def switch_tab(e):
                idx = e.control.selected_index
                if idx == 0: content_area.content = get_props_tab()
                elif idx == 1: content_area.content = get_buyers_tab()
                elif idx == 2: content_area.content = get_owners_tab()
                elif idx == 3: page.client_storage.remove("auth"); navigate("/login")
                page.update()

            return ft.View(route="/main", padding=0, controls=[content_area, ft.NavigationBar(destinations=[ft.NavigationDestination(icon="home", label="Props"), ft.NavigationDestination(icon="people", label="Buyers"), ft.NavigationDestination(icon="handshake", label="Owners"), ft.NavigationDestination(icon="logout", label="Exit")], on_change=switch_tab)])

        # 3. ADD PROPERTY VIEW
        def add_prop_view():
            title = ft.TextField(label="ခေါင်းစဉ်", border_radius=10)
            price = ft.TextField(label="ခေါ်ဈေး (သိန်း)", keyboard_type="number", border_radius=10)
            loc = ft.TextField(label="တည်နေရာ", border_radius=10)
            owner = ft.TextField(label="ပိုင်ရှင်အမည်", border_radius=10)

            def save_data(e):
                if not title.value or not price.value: return show_snack("အချက်အလက် ထည့်ပါ", "red")
                if API.insert("apk_properties", {"title": title.value, "asking_price": float(price.value), "location": loc.value, "owner_name": owner.value, "is_deleted": 0, "status": "Available"}):
                    show_snack("သိမ်းဆည်းပြီးပါပြီ"); navigate("/main")
                else: show_snack("Error", "red")

            return ft.View(route="/add_prop", bgcolor="white", controls=[ft.AppBar(title=ft.Text("အသစ်သွင်းရန်"), bgcolor="#1565C0", color="white", leading=ft.IconButton(icon="arrow_back", icon_color="white", on_click=lambda _: navigate("/main"))), ft.Container(padding=20, content=ft.Column([title, price, loc, owner, ft.ElevatedButton(text="Save Property", on_click=save_data, width=float('inf'), height=50, bgcolor="green", color="white")], spacing=15))])

        # ROUTING CORE
        def route_change(e):
            page.views.clear()
            if page.route == "/login": page.views.append(login_view())
            elif page.route == "/main": page.views.append(main_dashboard_view())
            elif page.route == "/add_prop": page.views.append(add_prop_view())
            else: page.views.append(login_view())
            page.update()

        page.route = "/login"
        route_change(None)

    # 4. SAFETY NET (WHITE SCREEN FIX)
    except Exception as e:
        error_msg = traceback.format_exc()
        page.add(
            ft.Container(padding=20, content=ft.Column([
                ft.Icon("error", color="red", size=50),
                ft.Text("Critical App Error (Not your phone's fault)", weight="bold", color="red"),
                ft.Text(error_msg, color="black", size=10, selectable=True)
            ]))
        )

if __name__ == "__main__":
    ft.app(target=main)
                
