import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.shortcuts import render, HttpResponse, redirect
from selenium import webdriver
from time import sleep
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from django.views.generic import View
from get2i.models import users, ids, ids_con
from django.core.exceptions import ObjectDoesNotExist
import requests
import os
from random import randint
from selenium.common.exceptions import StaleElementReferenceException

# heroku plugins:install heroku-repo
# heroku repo:purge_cache -a appname

# heroku run bash --app get2insta
# heroku ps:restart web.1
chromeOptions = Options()
chromeOptions.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chromeOptions.add_argument("--headless")
chromeOptions.add_argument("--disable-dev-sha-usage")
chromeOptions.add_argument("--no-sandbox")
# driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),
#                           chrome_options=chrome_options)
#
# chromeOptions = Options()
# chromeOptions.add_argument("--headless")
# chromeOptions.add_argument('--disable-gpu')
# chromeOptions.add_argument("--start-maximized")
# chromeOptions.add_argument("--disable-dev-sha-usage")
# chromeOptions.add_argument("--no-sandbox")


def flw_count(request):
    if request.method == 'POST':
        post_uname = request.POST['username']
        url = request.POST['url_1']
        try:
            u = users.objects.get(user_name=post_uname)
            if u:
                pass
        except ObjectDoesNotExist:
            u = users.objects.create(user_name=post_uname)
            insta_ids = ids_con.objects.all()
            for i in insta_ids:
                ids.objects.create(i_id=u, id_user=i.id_cons)
        r = requests.get(url).text

        start = '"edge_followed_by":{"count":'
        end = '},"followed_by_viewer"'
        followers = r[r.find(start) + len(start):r.rfind(end)]

        return HttpResponse(followers)
    else:
        return HttpResponse("Something Went Wrong Check Your Username")


class Insta_Bot(View):
    template_name = "get2insta/index.html"

    def post(self, *args, **kwargs):
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chromeOptions)
        # driver = webdriver.Chrome()
        id_username = self.request.POST['username']
        id_url = self.request.POST['url_1']
        self.id_username = id_username
        self.id_url = id_url
        self.driver = driver

        u = users.objects.get(user_name=id_username)
        try:
            c = ids.objects.filter(i_id=u)
            d = (len(c) - 1)
            if d == -1:
                return HttpResponse("Our Insta ID's Outdated We Are Updating Them To Give You More")
            elif d == 0:
                ides = c[0].id_user
                print(ides)
            else:
                r = randint(0, d)
                ides = c[r].id_user
                print(ides)
        except ValueError:
            return HttpResponse("Please Try Again...")

        return self.login_it(uname=ides, pw='Kartik@777', url=id_url)

    def login_it(self, uname, pw, url):
        self.driver.get(url)
        self.uname = uname
        sleep(1)
        try:
            self.driver.find_element_by_link_text("Follow").click()
        except NoSuchElementException or ElementClickInterceptedException:
            sleep(1)
            self.driver.find_element_by_link_text("Follow").click()
        sleep(1)
        email_input = self.driver.find_element_by_name("username")
        password_input = self.driver.find_element_by_name("password")
        email_input.send_keys(uname)
        password_input.send_keys(pw)
        sleep(2)
        self.driver.find_element_by_xpath('/html/body/div[5]/div[2]/div[2]/div/div/div[1]/div/form/div[4]/button') \
            .click()
        print("Logged In")
        u = users.objects.get(user_name=self.id_username)
        ids.objects.get(i_id=u, id_user=self.uname).delete()
        try:
            not_now = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button')
            if not_now:
                sleep(1)
                ActionChains(self.driver).move_to_element(not_now).click(not_now).perform()
                sleep(4)
                return self.follow_him()
        except (ElementClickInterceptedException, StaleElementReferenceException, NoSuchElementException):
            sleep(4)
            return self.follow_him()

    def follow_him(self):
        i = 0
        try:
            if i == 0:
                flw_btn = self.driver.find_element_by_xpath(
                    '//*[@id="react-root"]/section/main/div/header/section/div[2]/div/span/span[1]/button')
                if flw_btn:
                    ActionChains(self.driver).move_to_element(flw_btn).click(flw_btn).perform()
                    print("Ipad_Mobile Followed")
        except (ElementClickInterceptedException, NoSuchElementException):
            try:
                if i == 0:
                    flw_btn = self.driver.find_element_by_xpath(
                        '//*[@id="react-root"]/section/main/div/header/section/div[1]/div[1]/span/span[1]/button')
                    if flw_btn:
                        ActionChains(self.driver).move_to_element(flw_btn).click(flw_btn).perform()
                        print("PCFollowed")
            except (ElementClickInterceptedException, NoSuchElementException):
                try:
                    if i == 0:
                        flw_btn = self.driver.find_element_by_xpath(
                            '//*[@id="react-root"]/section/main/div/header/section/div[1]/button')
                        if flw_btn:
                            sleep(0.2)
                            ActionChains(self.driver).move_to_element(flw_btn).click(flw_btn).perform()
                            print("Private Account Followed")
                except (ElementClickInterceptedException, NoSuchElementException):
                    try:
                        if i == 0:
                            unflw_btn = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/div[2]/span/span[1]/button')
                            if unflw_btn:
                                print("Account Already Followed")
                    except (ElementClickInterceptedException, NoSuchElementException):
                        return HttpResponse("Instagram Has Restrict Our Account Please Try Again...")
        self.driver.close()
        return HttpResponse("You Just Got 1 Real & Genuine Followers")


def mail_us(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['msg']

        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        html = """
            <html>
              <head></head>
              <body>
                <h1>Hi Prince</h1>
                <p>You Just Got An Email From %s. Please Mail Him Back On %s.</p>
                <p>His Message Is : %s</p>
              </body>
            </html>
            """ % (name, email, message)
        part2 = MIMEText(html, 'html')
        msg.attach(part2)
        smtp_server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        smtp_server.login('guptapz111@gmail.com', '(Kartik@737)')
        smtp_server.sendmail("guptapz111@gmail.com", 'itz.kartik7@gmail.com', msg.as_string())
        smtp_server.close()
        return redirect('index')
    else:
        e = 'Please Try Again Later...'
        return render(request, 'get2i/index.html', {'e': e})
