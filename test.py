# def ssweb(url):

#     global currentDate, realCurrentDate
#     # currentDate = str(datetime.datetime.now().time())
#     # datenow = currentDate.replace(":","")
#     # realCurrentDate = datenow

#     rawinputstring = ""

#     if url.startswith("/instagram"):
#         rawinputstring = "www.instagram.com/"
#         rawinputstring += url.replace("/instagram", "")
#     if url.startswith("/screenshot"):
#         rawinputstring = url.replace("/screenshot", "")

#     inputstring = rawinputstring.replace(" ", "")


#     print(inputstring)
#     # print("http://"+inputstring)
#     # print("http://instagram.com/"+inputstring)
#     # return
#     try:
#         # options = webdriver.ChromeOptions()
#         # # options.add_argument('--ignore-certificate-errors')
#         # # options.add_argument("--test-type")
#         # options.add_argument("--headless")
#         # options.add_argument('--disable-gpu')
#         # # options.add_argument('disable-infobars')
#         # options.add_argument('--no-sandbox')
#         # options.add_argument('--start-maximized')
#         # # options.add_argument('--disable-dev-shm-usage')
#         # options.add_argument('--window-size=1366,768')
#         # if url.startswith("/instagram"):
#         #     options.add_argument('--window-size=480,720')
#         # options.add_argument('--screenshot --window-size=412,732 https://www.google.com/')
#         # options.binary_location = "/app/.apt/usr/bin/google-chrome"

#         # driver = webdriver.Chrome(executable_path="/app/.chromedriver/bin/chromedriver", chrome_options=options)
#         ##
#         # webFile = "https://trombosit.herokuapp.com/static/" + realCurrentDate + ".png"

#         if inputstring.startswith("https://"):
#             print("HTTPS Input:", inputstring)
#         elif inputstring.startswith("http://"):
#             print("HTTP Input:",inputstring)
#         els:
#             print("No HTTP input: "+ "http://" + inputstring)

#         if url.startswith("/instagram"):
#             print("Instagram input:", 'https://' + inputstring)


#         # if url.startswith("/instagram"):
#             # driver.find_element_by_class_name('.Szr5J').click()
#             # driver.find_element_by_css_selector('.Szr5J').click()
            

#         # print("Getting screenshot")
#         # driver.get_screenshot_as_file("static/" + realCurrentDate + ".png")
#         # driver.save_screenshot("static/ss.png")
#         # driver.close()
#         # print("Closing screenshot")
#         # return str(webFile)
        
#     except Exception as e:
#         print("Error :", e)
#         return None

# ssweb("/screenshot http://www.google.com")
# ssweb("/screenshot https://games.gemscool.com")
# ssweb("/screenshot www.gymoogle.com")
# ssweb("/instagram aryadytm12")