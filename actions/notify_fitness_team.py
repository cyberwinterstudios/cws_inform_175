from st2common.runners.base_action import Action
from email.message import EmailMessage

import smtplib


class NotifyFitness(Action):
    def __init__(self, *args, **kwargs):
        super(NotifyFitness, self).__init__(*args, **kwargs)
        self.smtp_server = self.config['smtp_server']
        self.smtp_port = int(self.config['smtp_port'])
        self.smtp_user = None
        self.smtp_pass = None
        if self.config.get('smtp_user') and self.config.get("smtp_password"):
            self.smtp_user = self.config['smtp_user']
            self.smtp_pass = self.config['smtp_password']
        self.from_address = self.config['from_address']
        self.to_address = self.config['to_address']

    def run(self, name, category, abs_score, push_score, sit_score, run_score, overall_score):
        msg = EmailMessage()

        msg['From'] = self.from_address
        msg['To'] = self.to_address
        msg['Subject'] = f"{name} Fitness Scorecard Results"

        body = f'Airman {name} has completed a fitness exam with an outcome of {category}. Detailed score information below:\n\n' \
               f'Abdominal Score: {abs_score}\nPush Up Score: {push_score}\nSit Up Score: {sit_score}\nRun/Walk Score: {run_score}\nOverall Score: {overall_score}'

        msg.set_content(body)

        with smtplib.SMTP(self.smtp_server, port=self.smtp_port) as smtp_server:
            smtp_server.ehlo()

            if self.smtp_port == 587:
                smtp_server.starttls()
            if self.smtp_user:
                smtp_server.login(user=self.smtp_user, password=self.smtp_pass)
            smtp_server.send_message(msg=msg)
