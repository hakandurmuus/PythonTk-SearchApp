import ttkbootstrap as tb
import requests
from PIL import Image, ImageTk
from decimal import Decimal
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup
import tkinter as tk
import webbrowser
import wikipedia


class App:
    def __init__(self):
        load_dotenv()
        self.window = tb.Window()
        self.window.geometry("1100x700+500+120")
        self.window.title("News")

        self.topbar = tb.Frame(self.window,bootstyle="info",height=100)
        self.topbar.pack(side="top",fill="x")

        self.leftbar = tb.Frame(self.window, bootstyle="secondary",width=300)
        self.leftbar.pack(side="left",fill="y")

        self.main = tb.Frame(self.window, bootstyle="light")
        self.main.pack(side="left",fill="both",expand=True)


        # --------------------------------------- ÜST BÖLÜM ---------------------------

        self.logo = tb.Label(self.topbar, text="NEWS.COM", font=50, bootstyle="inverse-danger",padding=10)
        self.logo.pack(side="left",padx=(75,0),pady=27)

        # ----Hava Durumu Bölümü-------
        self.weather()
        weather_ico = Image.open("icons/weathericon.ico")
        weather_ico = weather_ico.resize((60,60))
        self.weather_ico_img = ImageTk.PhotoImage(weather_ico)

        self.hava_icon_lbl = tb.Label(self.topbar,image=self.weather_ico_img)
        self.hava_icon_lbl.pack(side="left",padx=(100,0))
        self.sehir_lbl = tb.Label(self.topbar,text=self.sehir,bootstyle="inverse-danger")
        self.sehir_lbl.pack(side="left",pady=5,padx=5)
        self.hava_lbl = tb.Label(self.topbar,text=f"{self.hava} °C",bootstyle="inverse-danger")
        self.hava_lbl.pack(side="left",pady=5,padx=5)
        self.havainfo_lbl = tb.Label(self.topbar,text=self.hava_info,bootstyle="inverse-danger")
        self.havainfo_lbl.pack(side="left",pady=5,padx=5)
        # ----Hava Durumu Bölümü Son-------
        

        # ------Döviz Bölümü---------
        self.döviz()
        döviz_ico = Image.open("icons/döviz.ico")
        döviz_ico = döviz_ico.resize((60,60))
        self.döviz_ico_img = ImageTk.PhotoImage(döviz_ico)

        self.döviz_icon_lbl = tb.Label(self.topbar,image=self.döviz_ico_img)
        self.döviz_icon_lbl.pack(side="left",pady=5,padx=(30,0))
        self.dolar_lbl = tb.Label(self.topbar,text=f"USD:{self.usd}",bootstyle="inverse-danger")
        self.dolar_lbl.pack(side="left",pady=5,padx=5)
        self.euro_lbl = tb.Label(self.topbar,text=f"EUR:{self.eur}",bootstyle="inverse-danger")
        self.euro_lbl.pack(side="left",pady=5,padx=5)
        self.sterlin_lbl = tb.Label(self.topbar,text=f"GBP:{self.gbp}",bootstyle="inverse-danger")
        self.sterlin_lbl.pack(side="left",pady=5,padx=5)
        self.renminbi_lbl = tb.Label(self.topbar,text=f"CNY:{self.cny}",bootstyle="inverse-danger")
        self.renminbi_lbl.pack(side="left",pady=5,padx=5)
        # --------Döviz Bölümü Son------------

        # --------------------------------------- ÜST BÖLÜM SONU---------------------------

        # --------------------------------------- SOL BÖLÜM -------------------------------

        self.search_ent = tb.Entry(self.leftbar,width=35)
        self.search_ent.pack(padx=5,pady=5)

        self.search_btn = tb.Button(self.leftbar,text="Ara",command=self.search)
        self.search_btn.pack()

        leftbar_scrool_right = tb.Scrollbar(self.leftbar,orient="vertical")
        leftbar_scrool_right.pack(fill="y",side="right")
        leftbar_scrool_bottom = tb.Scrollbar(self.leftbar,orient="horizontal")
        leftbar_scrool_bottom.pack(fill="x",side="bottom")

        self.search_resuts_list = tk.Listbox(self.leftbar,width=35,height=200,
                                             yscrollcommand=leftbar_scrool_right.set,
                                             xscrollcommand=leftbar_scrool_bottom.set)
        self.search_resuts_list.pack(pady=5,padx=2,fill="y")

        leftbar_scrool_right.config(command=self.search_resuts_list.yview)
        leftbar_scrool_bottom.config(command=self.search_resuts_list.xview)

        self.search_resuts_list.bind("<Double-Button-1>",self.show_details)

        # --------------------------------------- SOL BÖLÜM SONU -------------------------------



        # --------------------------------------- ORTA BÖLÜM -------------------------------

        self.content_txt = tb.Text(self.main,height=50)
        self.content_txt.pack(fill="both")     

        dosya = "document.txt"
        if dosya:
            with open(dosya,"r",encoding="utf-8") as file:
                icerik = file.read()
            
            self.content_txt.delete("1.0",tk.END)
            self.content_txt.insert("end","Hoşgeldiniz")
            self.content_txt.tag_add("baslik","1.0","1.end")
            self.content_txt.tag_configure("baslik", font=("Arial", 16, "bold"),justify="center")
            self.content_txt.insert(tk.END,icerik)

        # --------------------------------------- ORTA BÖLÜM SONU-------------------------------


        self.window.mainloop()


    def weather(self):
        url = "http://api.weatherapi.com/v1/current.json"
        weather_api_key = os.getenv("weather")
        sehir = "Bursa"

        response = requests.get(url, params= {
            "key":weather_api_key,
            "q":sehir,
            "lang":"tr"
        })
        sonuc = response.json()

        self.sehir = sonuc["location"]["name"]
        self.hava = sonuc["current"]["temp_c"]
        self.hava_info = sonuc["current"]["condition"]["text"]
        self.hava_icon = sonuc["current"]["condition"]["icon"]

    def döviz(self):
        döviz_apı_key = os.getenv("döviz")
        url = f"https://v6.exchangerate-api.com/v6/{döviz_apı_key}/latest/TRY"
        response = requests.get(url)
        sonuc = response.json()
        self.usd = round(Decimal(1/(sonuc["conversion_rates"]["USD"])),3)
        self.eur = round(Decimal(1/(sonuc["conversion_rates"]["EUR"])),3)
        self.gbp = round(Decimal(1/(sonuc["conversion_rates"]["GBP"])),3)
        self.cny = round(Decimal(1/(sonuc["conversion_rates"]["CNY"])),3)
        
    def search(self):
        self.search_input = self.search_ent.get()
        news_api_key = os.getenv("news")
        everything_url = "https://newsapi.org/v2/everything"

        response = requests.get(everything_url,params={
            "apiKey":news_api_key,
            "q":self.search_input,
            "language":"tr",
            "sortBy": "publishedAt"
        })

        self.haberler = response.json()["articles"]

        self.search_resuts_list.delete(0,"end")
        self.search_resuts_list.insert(tk.END,"wikipedia")
        for i in self.haberler:
            self.news_site = i["source"]["name"]
            self.news_title = i["title"]
            self.news_url = i["url"]
            self.content = i["content"]
            haber = f"{self.news_site} - {self.news_title} - {self.news_url}"
            self.search_resuts_list.insert(tk.END,haber)
            
        
    def show_details(self, event):
        for widget in self.main.winfo_children():
            widget.destroy()
        self.open_btn = tb.Button(self.main,text="Tarayıcıda aç",command=self.open_browser)
        self.open_btn.pack(side="top",pady=2)
        self.main_scroll_right = tb.Scrollbar(self.main,orient="vertical")
        self.main_scroll_right.pack(fill="y",side="right")
        self.main_scroll_bottom = tb.Scrollbar(self.main,orient="horizontal")
        self.main_scroll_bottom.pack(fill="x",side="bottom")
        self.content_txt = tb.Text(self.main,height=50,
                                   yscrollcommand=self.main_scroll_right.set,
                                   xscrollcommand=self.main_scroll_bottom.set)
        self.content_txt.pack(fill="both")
        self.main_scroll_right.config(command=self.content_txt.yview)
        self.main_scroll_bottom.config(command=self.content_txt.xview)

        self.content_txt.delete("1.0","end")
        self.idx = self.search_resuts_list.curselection()
        self.idx = self.idx[0]
        if self.idx == 0:
            wikipedia.set_lang("tr")
            result = wikipedia.page(self.search_input)
            self.content_txt.insert(0.0,self.search_input.upper() + "\n\n")
            self.content_txt.tag_add("baslik","1.0","1.end")
            self.content_txt.tag_configure("baslik", font=("Arial", 16, "bold"),justify="center")
            self.content_txt.insert("end",result.content)
        else:
            article = self.haberler[self.idx-1]
            self.article_url = article["url"]
            print(self.article_url)

            response = requests.get(self.article_url, timeout=5)
            soup = BeautifulSoup(response.content,"html.parser")
            paragraphs = soup.find_all("p")
            content = "\n".join(p.get_text() for p in paragraphs)
            if not content.strip():
                content = "Haber içeriği alınamadı."
            
            self.content_txt.insert("end",f"Yazar: {article["author"]}\n\n")
            self.content_txt.insert("end",f"Başlık: {article["title"]}\n\n")
            self.content_txt.insert("end",f"Özet: {article["description"]}\n\n")
            self.content_txt.insert("end",f"İçerik:\n{content}")


    def open_browser(self):
        if self.idx == 0:
            wiki_url = "https://tr.wikipedia.org/wiki/" + self.search_input.title().replace(' ','_')
            webbrowser.open(wiki_url)
        else:    
            webbrowser.open(self.article_url)



app = App()

