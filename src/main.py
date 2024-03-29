from datetime import datetime
import requests as r
from bs4 import BeautifulSoup as bs
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import logging

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s [%(name)-12s] %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG) 

class Html_Elements:
    def __init__(self, *args):
        pass

class Scraper:

    def __init__(self, url, css_selector) -> None:
        self.url = url
        self.css_selector = css_selector
        self.html = ""

    def get_html(self):
        html = r.get(self.url, allow_redirects=True)
        self.html = html.text if html.status_code == 200 else "No data"

        logging.error("get_html No data")
        
    
    def parse_html_by_css_selector(self):
        self.html_parsed = bs(self.html, 'html.parser').select(self.css_selector)
    
class Mail_Provider:
    def __init__(self, sender, password, receiver, subject, body):
        self.sender = sender
        self.password = password
        self.receiver = receiver
        self.subject = subject
        self.body = body
        self.message = ""
    
    def build_message(self):
        message = MIMEMultipart()
        message["from"] = self.sender
        message["to"] = self.receiver
        message["subject"] = self.subject

        message.attach(MIMEText(self.body, "html"))

        self.message = message.as_string()

    
    def send_mail(self):
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context = ssl.create_default_context()) as server:
            server.login(self.sender, self.password)
            errors = server.sendmail(self.sender, self.receiver, self.message)

            logger.info("Successfully delivered") if len(errors) == 0 else logger.error(f"Something terrible happend while sending mail. Errors: {errors}")

def run():
    scraper = Scraper("https://eumetsat.jobbase.io", 'div[class="cell-table col-sm-17 col-xs-20"] > div > h3 > a')

    scraper.get_html()
    scraper.parse_html_by_css_selector()

    vacancies, file_links = [v.text for v in scraper.html_parsed], [(scraper.url + f['href']) for f in scraper.html_parsed]

    table_html = [f"<tr> <td> {i[0]} </td> <td> {i[1]} </td> </tr>" for i in tuple(zip(vacancies, file_links))]

    msg ="<!DOCTYPEhtml><html><head><style>table{font-family:arial,sans-serif;}td,th{border:1pxsolid#dddddd;text-align:left;padding:8px;}tr:nth-child(even){background-color:#dddddd;}</style></head>"

    msg_body = "<body><h2>Available Positions at EUMETSAT</h2><p>You'll be a part of this someday, so keep working every day!</p>  <table>   <tr>     <th>Position</th>     <th>Link</th>  %s  </table>  </body> </html>" %"".join(table_html)

    msg += msg_body

    mail_provider = Mail_Provider("jobupdatesfromeumetsat@gmail.com", 
                                  "scjpagonkjqozalo", 
                                  "berkesenturk11@gmail.com", 
                                  "EUMETSAT Vacancies on {}".format(datetime.today().strftime("%Y/%m/%d")), 
                                  msg)

    mail_provider.build_message()
    mail_provider.send_mail()

if __name__ == "__main__":
    run()