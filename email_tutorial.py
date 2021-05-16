import smtplib
from email.mime.text import MIMEText

# 'darios.tbot.notifier@gmail.com'

sender = 'darios.tbot.notifier@gmail.com'
receivers = 'darios.tbot.notifier@gmail.com'

msg = MIMEText('This is test mail')
msg['Subject'] = 'Test Mail'
msg['From'] = sender
msg['To'] = receivers

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server: 
    server.login(sender, 'Hasi4589')
    server.sendmail(from_addr=sender, to_addrs=receivers, msg=msg.as_string())
    print('successfully sent email')
    server.quit()