from asyncio.windows_events import NULL
from selenium import webdriver
import time
import tkinter as tk
from requests import get

window = tk.Tk()
window.geometry("300x200")
window.resizable(False, False)
window.title("IPChanger")
# window.iconbitmap('./files/icon.ico')

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")


def getIp():
    try:
        ipLabel.config(text="İp adresiniz : " +
                       get('https://api.ipify.org/').content.decode('utf8'))
    except:
        ipLabel.config(text="İnternet Bağlantınızı Kontrol Edin !")


def getElement(xpath, driver):
    for i in range(5):
        time.sleep(1)
        element = driver.find_element_by_xpath(xpath)
        if (element != NULL):
            return element
        elif (i == 5):
            return 0


def setStatus(text):
    statusLabel.config(text=text)


def change():
    driver = webdriver.Chrome(chrome_options=options)

    for i in range(5):
        try:
            setStatus("Panele giriliyor")
            driver.get("http://192.168.1.1/")
            time.sleep(1)
            break
        except:
            setStatus('Adres Başlatılamadı ! Deneme ', i+1)
            if (i == 4):
                setStatus("Başarısız !")
                driver.close()
                return

    for i in range(5):
        if (driver.current_url == "http://192.168.1.1/login"):
            setStatus("Giriş deneniyor")

            username = driver.find_element_by_xpath('//*[@id="username"]')
            password = driver.find_element_by_xpath('//*[@id="userpassword"]')
            loginBtn = driver.find_element_by_xpath('//*[@id="loginBtn"]')

            if (username == 0 or password == 0 or loginBtn == 0):
                setStatus("Başarısız !")
                return 0

            username.send_keys("admin")
            password.send_keys("123789546b.B")

            time.sleep(1)
            loginBtn.click()
            time.sleep(1)

            setStatus("Giriş Yapıldı")
            break

    for i in range(5):
        try:
            setStatus("Broadband ayarlarına giriliyor")
            driver.get("http://192.168.1.1/Broadband")
            time.sleep(2)
            break
        except:
            setStatus('Adres Başlatılamadı ! Deneme ' + i+1)
            if (i == 4):
                setStatus("Başarısız !")
                driver.close()
                return

    for i in range(5):
        try:
            setStatus("Network ayarlarına giriliyor")
            editBtn = driver.find_element_by_xpath(
                '/html/body/div/div/div[4]/div/div[2]/div/div/div[2]/table/tbody/tr/td[13]/span[1]/i')
            editBtn.click()
            time.sleep(2)
        except:
            setStatus('Buton bulunamadı ! Deneme ' + i+1)
            if (i == 4):
                setStatus("Başarısız !")
                driver.close()
                return

        try:
            setStatus("Network ayarları kaydediliyor")
            saveBtn = driver.find_element_by_xpath(
                '//*[@id="WANInterface_btnsave"]')
            saveBtn.click()
            break
        except:
            setStatus("Ayarlar kaydedilemedi ! Deneme " + i+1)
            if (i == 4):
                setStatus("Başarısız !")
                driver.close()
                return

    setStatus("Başarılı !")
    getIp()
    driver.close()


startButton = tk.Button(window, text="IP DEĞİŞTİR", bg="gray",
                        fg="white", border="0", activebackground="#A9A9A9", command=change)
startButton.pack()
startButton.place(anchor="n", height=75, width=250, x=150, y=25)

statusLabel = tk.Label(window, text="Boşta")
statusLabel.pack()
statusLabel.place(anchor="n", x=150, y=110)

ipLabel = tk.Label(window, text="İp adresiniz : ")
ipLabel.pack()
ipLabel.place(anchor="n", x=155, y=135)

startButton = tk.Button(window, text="Ip Güncelle", bg="gray",
                        fg="white", border="0", activebackground="#A9A9A9", command=getIp)
startButton.pack()
startButton.place(anchor="n", height=25, width=75, x=155, y=160)

# Start the GUI
window.mainloop()
