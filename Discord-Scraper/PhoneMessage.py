import smtplib
carriers = {
    'att':    '@mms.att.net',
    'tmobile':' @tmomail.net',
    'verizon':  '@vtext.com',
    'sprint':   '@page.nextel.com'
}

def send(message_text):

    fromaddr = 'pwilda100@gmail.com'
    toaddr = ['4804630030@tmomail.net','4807346105@vtext.com']
    cc = ['test@gmail.com','wildakids@gmail.com']
    message_subject = 'TRADE UPDATE'

    message = ("From: %s \r\n" % fromaddr
    + "To: %s \r\n" % ",".join(toaddr)
    + "CC: %s\r\n" % ",".join(cc)
    + "Subject: %s\r\n" % message_subject
    + "\r\n" 
    + message_text)

    # Replace the number with your own, or consider using an argument\dict for multiple people.
	#to_number = '4804630030{}'.format(carriers['tmobile'])
    #to_number = 'wildakids@gmail.com'

    try:
        auth = ('pwilda100@gmail.com','legoswag1441')
        # Establish a secure session with gmail's outgoing SMTP server using your gmail account
        server = smtplib.SMTP( "smtp.gmail.com", 587 )
        server.starttls()
        #if things break uncomment line below to debug
        #server.set_debuglevel(1)
        server.login(auth[0], auth[1])
	    # Send text message through SMS gateway of destination number
        server.sendmail( auth[0], toaddr, message)
        server.quit()
        print("EMAIL SENT")

    except:
        print("Something went wrong...")

#send("we made billions")

