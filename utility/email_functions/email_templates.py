WELCOME_MAIL_TEMPLATE = '''
<html>
<body>
  <div style="display: flex; justify-content: center; align-items: center; height: 100vh;">
    <div style="padding-top: 2rem;"">
      <img style="width: 100%;" src="https://i.imgur.com/oE2zcEO.png" />
      <div style="border-top-width: 1px; margin-left: 5%; margin-right: 5%;">
        <div style="padding-bottom: 1rem; border-top-width: 1px; font-size: 1rem;line-height: 0.75rem; line-height: 1.75rem; ">
            <h3 style="padding-bottom: 0; margin-bottom: 0;" >Hii {first_name}, Welcome to BlueLabs</h3><br>
            <p style="padding-top: 0; margin-top: 0; font-size: 0.875rem;line-height: 1.25rem;">Current Tools/Offerings</p>
            <ul style="margin-top: 0.5rem; ">
              <li><p>Notion Widgets</p></li>
              <li><p>Notes</p></li>
            </ul>
            <p style="font-size: 0.875rem; line-height: 1.25rem; font-weight: 200;">Hi, I'm Ankit, and I create things that I like.</p>
            <p><a href="https://www.linkedin.com/in/ankit69/">Contact me</a></p>
        </div>
      </div>
    </div>
  </div>
  <div style="height: 15vh; widht: 100vw"></div>
</body>
</html>
'''


# Creating a list of Temp Emails
TEMP_EMAIL_LIST = []
temp_email_file = open('utility//email_functions//disposable_email_blocklist.conf', 'r')
Emails = temp_email_file.readlines()
# Strips the newline character
for Email in Emails:
    TEMP_EMAIL_LIST.append(Email.strip())
temp_email_file.close()
