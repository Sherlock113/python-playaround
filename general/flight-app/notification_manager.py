import smtplib


class NotificationManager:

    def __init__(self):
        self.my_email = "xxx@gmail.com"
        self.password = "***"

    def send_email(self):
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls() 
            connection.login(user=self.my_email, password=self.password)
            connection.sendmail(
                from_addr=self.my_email,
                to_addrs="xxx@gmail.com",
                msg="Subject:Hello\n\nThe flight ticket is cheaper. Buy it now!"
            )
        # Code to be finished
