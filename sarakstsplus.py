    # nepieciešamās bibliotēkas imports
import tkinter as tk
import json
from tkinter import messagebox


class SarakstsPlusApp:
    # klases konstruktors, kas inicializē galvenos lietotnes parametrus, izveido galveno saskarni-izvēlni un pievieno pogas
    def __init__(self, master):
        # lietotnes pamatparametru inicializācija, veidojot klases gadījumu
        self.master = master
        self.master.title("Saraksts+")
        self.master.geometry("375x667") # ekrānas izmērs noradīts "in points", nevis "in pixels" (2 points = 1 pixel)
        self.current_interface = "Home"
        # metode datu ielādei no JSON faila
        self.schedule_data = self.load_schedule_data()

        # galvenās saskarnes izveide
        self.menu_frame = tk.Frame(self.master)
        self.menu_frame.pack()

        # pogu pievienošana galvenajai saskarnei
        tk.Button(self.menu_frame, text="Saraksti", command=self.show_schedules, height=5, width=20, font=("Arial", 20)).pack(pady=15)
        tk.Button(self.menu_frame, text="Pieturas", command=self.show_stops, height=5, width=20, font=("Arial", 20)).pack(pady=15)
        tk.Button(self.menu_frame, text="Māja", command=self.show_home, height=5, width=20, font=("Arial", 20)).pack(pady=15)

    # šī metode ielādē datus no JSON faila
    def load_schedule_data(self):
        try:
            with open("schedule_data.json", "r", encoding='utf-8') as file:
                schedule_data = json.load(file)
            return schedule_data
        # ja fails netiek atrasts, tiek parādīts brīdinājums
        except FileNotFoundError:
            messagebox.showwarning("Kļūda!", "Fails schedule_data.json nav atrasts.")
            return {}

    # parāda saskarni ar dažādu maršrutiem
    def show_schedules(self):
        self.clear_frame()
        self.current_interface = "Schedules"

        schedules_frame = tk.Frame(self.master)
        schedules_frame.pack()

        # katram maršrutam izveido freimu ar etiķetēm un pogām. Katra poga izsauc show_stops ar atbilstošo maršrutu

        tk.Label(schedules_frame, text="Visi", font=("Arial", 16)).pack(pady=10)
        tk.Button(schedules_frame, text="🚊 1: Imanta - Jugla", command=lambda: self.show_stops("🚊 1: Imanta - Jugla", ),font=("Arial", 12)).pack(pady=5)
        tk.Button(schedules_frame, text="🚊 2: Stacijas laukums - Tapešu iela", command=lambda: self.show_stops("🚊 2: Stacijas laukums - Tapešu iela"),font=("Arial", 12)).pack(pady=5)
        tk.Button(schedules_frame, text="🚊 5: Iļģuciems - Mīlgrāvis", command=lambda: self.show_stops("🚊 5: Iļģuciems - Mīlgrāvis"),font=("Arial", 12)).pack(pady=5)
        tk.Button(schedules_frame, text="🚊 7: Ausekļa iela - Ķengarags", command=lambda: self.show_stops("🚊 7: Ausekļa iela - Ķengarags"),font=("Arial", 12)).pack(pady=5)
        tk.Button(schedules_frame, text="🚊 10: Stacijas laukums - Bišumuiža", command=lambda: self.show_stops("🚊 10: Stacijas laukums - Bišumuiža"),font=("Arial", 12)).pack(pady=5)
        tk.Button(schedules_frame, text="🚊 11: Ausekļa iela - Mežaparks", command=lambda: self.show_stops("🚊 11: Ausekļa iela - Mežaparks"),font=("Arial", 12)).pack(pady=5)
        tk.Button(schedules_frame, text="🚎 1: Valmieras iela - Pētersalas iela", command=lambda: self.show_stops("🚎 1: Valmieras iela - Pētersalas iela"),font=("Arial", 12)).pack(pady=5)
        tk.Button(schedules_frame, text="🚎 3: Centrāltirgus - Sarkandaugava", command=lambda: self.show_stops("🚎 3: Centrāltirgus - Sarkandaugava"),font=("Arial", 12)).pack(pady=5)
        tk.Button(schedules_frame, text="🚎 4: Jugla - Ziepniekkalns", command=lambda: self.show_stops("🚎 4: Jugla - Ziepniekkalns"),font=("Arial", 12)).pack(pady=5)
        tk.Button(schedules_frame, text="🚎 9: Stacijas laukums - Iļģuciems", command=lambda: self.show_stops("🚎 9: Stacijas laukums - Iļģuciems"),font=("Arial", 12)).pack(pady=5)
        tk.Button(schedules_frame, text="🚎 11: Centrālā stacija - Ieriķu iela", command=lambda: self.show_stops("🚎 11: Centrālā stacija - Ieriķu iela"),font=("Arial", 12)).pack(pady=5)

        # atgriež lietotāju galvenajā saskarnē, izmantojot pogu "Atpakaļ"
        tk.Button(schedules_frame, text="Atpakaļ", command=self.show_menu,font=("Arial", 12)).pack(pady=10)

    # parāda saskarni ar pieturām atlasītajam maršrutam
    def show_stops(self, route_name=None):
        self.clear_frame()
        self.current_interface = "Stops"

        # Остановки
        stops_frame = tk.Frame(self.master)
        stops_frame.pack()

        label_frame = tk.Frame(stops_frame)
        label_frame.pack(pady=10)

        stops_listbox = tk.Listbox(stops_frame, selectmode=tk.SINGLE, height=30, width=40)
        stops_listbox.pack(pady=10)

        # ja ir norādīts route_name, tiek parādīts izvēlētā maršruta pieturu saraksts
        if route_name:
            tk.Label(label_frame, text=f"{route_name}", font=("Arial", 16)).pack()

            for stop_name in self.schedule_data.get(route_name, {}):
                stops_listbox.insert(tk.END, stop_name)

            stops_listbox.bind('<Double-Button-1>', lambda event: self.show_schedule_times(route_name,stops_listbox.get(stops_listbox.curselection())))
            # poga "Atpakaļ" atgriež lietotāju uz iepriekšējo saskarni
            tk.Button(stops_frame, text="Atpakaļ", command=lambda: self.show_schedules(),font=("Arial", 12)).pack(pady=10)
        # saskarne "Pieturas" izmanto gadījumu, ja nav norādīts route_name
        else:
            tk.Label(stops_frame, text="Interaktīva karte (izslegta maketās programmā)").pack(pady=10)
            tk.Button(stops_frame, text="Pieturas meklēšana", command=self.show_unavailable_message).pack(pady=5)
            # poga "Atpakaļ" atgriež lietotāju galvenajā saskarnē
            tk.Button(stops_frame, text="Atpakaļ", command=lambda: self.show_menu()).pack(pady=10)

    # parāda saskarni ar laika izvēli konkrētai pieturai
    def show_schedule_times(self, route_name, stop_name):
        self.clear_frame()
        self.current_interface = "ScheduleTimes"

        # izveido freimu ar etiķetēm un pogām, lai izvēlētos dienas veidu (darba diena vai brīvdienas)
        schedule_times_frame = tk.Frame(self.master)
        schedule_times_frame.pack()

        tk.Label(schedule_times_frame, text=f"{stop_name}",font=("Arial", 16)).pack(pady=100)
        tk.Button(schedule_times_frame, text="Darba dienas",
                  command=lambda: self.show_schedule(route_name, stop_name, "Darba dienas"),font=("Arial", 12)).pack(pady=5)
        tk.Button(schedule_times_frame, text="Brīvdienas",
                  command=lambda: self.show_schedule(route_name, stop_name, "Brīvdienas"),font=("Arial", 12)).pack(pady=5)

        # poga "Atpakaļ" atgriež lietotāju uz iepriekšējo saskarni
        tk.Button(schedule_times_frame, text="Atpakaļ", command=lambda: self.show_stops(route_name),font=("Arial", 12)).pack(pady=100)

    # parāda sarakstu atlasītajai pieturai atkarībā no izvēlētā dienas veida (darba diena vai brīvdiena)
    def show_schedule(self, route_name, stop_name, day_type):
        self.clear_frame()
        self.current_interface = "Schedule"

        schedule_frame = tk.Frame(self.master)
        schedule_frame.pack()

        label_frame = tk.Frame(schedule_frame)
        label_frame.pack(pady=10)

        tk.Label(label_frame, text=f"{stop_name} - {day_type}",font=("Arial", 16)).pack(pady=50)

        # laika saraksta iegūšana no JSON datni
        times = self.schedule_data.get(route_name, {}).get(stop_name, {}).get(day_type, [])

        # 'listbox' izveidošana
        listbox = tk.Listbox(schedule_frame, selectmode=tk.SINGLE, height=20, width=40)
        listbox.pack(pady=10)

        # 'listbox' elementu pievienošana
        for time in times:
            listbox.insert(tk.END, time)

        # 'Scrollbar' izveidošana
        scrollbar = tk.Scrollbar(schedule_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)

        # poga "Atpakaļ" atgriež lietotāju uz iepriekšējo saskarni
        tk.Button(schedule_frame, text="Atpakaļ", command=lambda: self.show_schedule_times(route_name, stop_name),font=("Arial", 12)).pack(pady=10)

    # 'Māja' saskarnes izveidošana
    def show_home(self):
        self.clear_frame()
        self.current_interface = "Home"

        home_frame = tk.Frame(self.master)
        home_frame.pack()

        tk.Button(home_frame, text="Sazināties ar izstrādātāju", command=self.show_feedback,font=("Arial", 18)).pack(pady=10)
        tk.Button(home_frame, text="Reģiona izvelēšana", command=self.show_region_selection,font=("Arial", 18)).pack(pady=10)
        tk.Button(home_frame, text="Valodas izvelēšana", command=self.show_language_selection,font=("Arial", 18)).pack(pady=10)
        tk.Button(home_frame, text="Aplikācijas versija", command=self.show_version_info,font=("Arial", 18)).pack(pady=10)
        tk.Button(home_frame, text="Atpakaļ", command=self.show_menu,font=("Arial", 12)).pack(pady=170)

    # parāda saskarni, kur var sazināties ar izstrādātāju
    def show_feedback(self):
        self.clear_frame()
        self.current_interface = "Feedback"

        feedback_frame = tk.Frame(self.master)
        feedback_frame.pack()

        tk.Label(feedback_frame, text="Sazināties ar izstrādātāju",font=("Arial", 16)).pack(pady=10)
        tk.Label(feedback_frame, text="Uzrakstiet tematu:",font=("Arial", 12)).pack(pady=5)
        tk.Entry(feedback_frame,width=40).pack(pady=5)
        tk.Label(feedback_frame, text="Apraksts:",font=("Arial", 12)).pack(pady=5)
        tk.Text(feedback_frame, height=5, width=40).pack(pady=5)

        tk.Button(feedback_frame, text="Nosūtīt", command=lambda: self.show_home(),font=("Arial", 16)).pack(pady=100)
        tk.Button(feedback_frame, text="Atpakaļ", command=lambda: self.show_home(),font=("Arial", 12)).pack(pady=50)

    # parāda saskarni, kur var izvēlēties reģionu
    def show_region_selection(self):
        self.clear_frame()
        self.current_interface = "RegionSelection"

        region_frame = tk.Frame(self.master)
        region_frame.pack()

        # pašlaik var izvēlēties tikai vienu reģionu
        tk.Label(region_frame, text="Reģiona izvēlēšana",font=("Arial", 16)).pack(pady=10)
        tk.Button(region_frame, text="Rīga", command=lambda: self.show_home(),font=("Arial", 12)).pack(pady=100)
        tk.Button(region_frame, text="Atpakaļ", command=lambda: self.show_home(),font=("Arial", 12)).pack(pady=100)

    # parāda saskarni, kur var izvēlēties valodu
    def show_language_selection(self):
        self.clear_frame()
        self.current_interface = "LanguageSelection"

        language_frame = tk.Frame(self.master)
        language_frame.pack()

    # ir angļu valodas izvēlēšanas poga, taču pašlaik šū funkcija nav pieejama šajā programmas versijā
        tk.Label(language_frame, text="Valodas izvēlēšana",font=("Arial", 16)).pack(pady=10)
        tk.Button(language_frame, text="Latviešu valoda", command=lambda: self.show_home(),font=("Arial", 12)).pack(pady=5)
        tk.Button(language_frame, text="English language", command=self.show_unavailable_message,font=("Arial", 12)).pack(pady=5)
        tk.Button(language_frame, text="Atpakaļ", command=lambda: self.show_home(),font=("Arial", 12)).pack(pady=250)

    # parāda ziņojumu, kas norāda, ka funkcija nav pieejama
    def show_unavailable_message(self):
        messagebox.showinfo("Kļūda!", "Šī funkcija nav pieejama šajā programmas versijā!")

    # parāda saskarni, kur var aplūkot lietotnes versiju, kā arī ziņojumu lietotājām par lietotnes versiju
    def show_version_info(self):
        self.clear_frame()
        self.current_interface = "VersionInfo"

        version_frame = tk.Frame(self.master)
        version_frame.pack()

        tk.Label(version_frame, text="Jūs izmantojat maketas versiju!",font=("Arial", 19)).pack(pady=100)
        tk.Label(version_frame, text="Aplikācijas versija:", font=("Arial", 19)).pack(pady=1)
        tk.Label(version_frame, text="1.0.0t",font=("Arial", 19)).pack(pady=10)
        tk.Button(version_frame, text="Atpakaļ", command=lambda: self.show_home(),font=("Arial", 12)).pack(pady=100)

    # parāda galveno saskarni
    def show_menu(self):
        self.clear_frame()
        self.current_interface = "Menu"

        # Главное меню
        self.menu_frame = tk.Frame(self.master)
        self.menu_frame.pack()

        tk.Button(self.menu_frame, text="Saraksti", command=self.show_schedules, height=5, width=20, font=("Arial", 20)).pack(pady=15)
        tk.Button(self.menu_frame, text="Pieturas", command=self.show_stops, height=5, width=20, font=("Arial", 20)).pack(pady=15)
        tk.Button(self.menu_frame, text="Māja", command=self.show_home, height=5, width=20, font=("Arial", 20)).pack(pady=15)

    # no pašreizējā freima tiek noņemti visi logrīki
    def clear_frame(self):
        for widget in self.master.winfo_children():
            widget.destroy()

# lietotnes darbības sākšana
if __name__ == "__main__":
    root = tk.Tk()
    app = SarakstsPlusApp(root)
    root.mainloop()
