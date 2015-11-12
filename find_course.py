from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
from datetime import datetime
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import unicodedata
import platform
import smtplib
import getpass
import os
import sys
import time
 
def getUserInfo():

    GATORLINK_ID = str(raw_input('GatorLink Username: '))
    PASSWORD = str(getpass.getpass('Password:'))
    TERM = str(raw_input('Term (spring, summer, fall): '))
    COURSE = str(raw_input('Course (e.g. ENC1101): '))

    print('\nIf you want to be notified via text message when a course opens up')
    print('please input your phone number and carrier (e.g. 354-543-1234,att)')
    print('The supported carries are: att, tmobile, sprint, verizon, metropcs\n')
    print('If left blank you will be sent an email to your uf-email account.\n')

    CELL_INFO = str(raw_input('Cell phone number and carrier (cell-phone-number,carrier): '))
    
    global CELL_PROVIDED 
   
    if not CELL_INFO:

        CELL_PROVIDED = False

        return (GATORLINK_ID, PASSWORD, TERM, COURSE)

    else: 

        CELL_PROVIDED = True

        CELL = CELL_INFO.split(',')[0]

        if ' ' in CELL:
            CELL = CELL.replace(' ','')

        if('-' in CELL):
            CELL = CELL.replace('-','')

        CARRIER = CELL_INFO.split(',')[1]
        
        return (GATORLINK_ID, PASSWORD, TERM, COURSE, (CELL,CARRIER))

def sendText(user_info):

    if (str(user_info[4][1])) == 'att':

        to = str(user_info[4][0])+'@txt.att.net'
    
    elif (str(user_info[4][1])) == 'tmobile':

        to = to = str(user_info[4][0])+'@tmomail.net' 
    
    elif (str(user_info[4][1])) == 'sprint':

        to = to = str(user_info[4][0])+'@messaging.sprintpcs.com' 

    elif (str(user_info[4][1])) == 'verizon':

        to = to = str(user_info[4][0])+'@vtext.com' 

    elif (str(user_info[4][1])) == 'metropcs':

        to = to = str(user_info[4][0])+'@mymetropcs.com'

    else:

        print('Carrier not supported. An email will be sent your uf-email account.')

        return sendEmail(user_info)

    print('A spot opened up for your class!')
    print('Sending notification text message.')

    office365_user = str(user_info[0])+'@ufl.edu'

    office365_pwd = str(user_info[1])

    #Set up server to send text message when course is found
    smtpserver = smtplib.SMTP("smtp.office365.com",587)

    smtpserver.ehlo()

    smtpserver.starttls()

    smtpserver.ehlo()

    smtpserver.login(office365_user,office365_pwd)
    
    msg = """
    \nA spot opened up for your course (%s) \nLogin to ISIS and register before someone else takes it!
          """ %user_info[3]
    
    smtpserver.sendmail(office365_user, to, msg)
    
    smtpserver.close()

def sendEmail(user_info):

    print('A spot opened up for your class!')
    print('Sending notification email.')
    
    to = str(user_info[0])+'@ufl.edu'

    office365_user = str(user_info[0])+'@ufl.edu'

    office365_pwd = str(user_info[1])

    #Set up server to send text message when course is found
    smtpserver = smtplib.SMTP("smtp.office365.com",587)

    smtpserver.ehlo()

    smtpserver.starttls()

    smtpserver.ehlo()

    smtpserver.login(office365_user,office365_pwd)
    
    msg = """
    \nA spot opened up for your course (%s) \nLogin to ISIS and register before someone else takes it!
          """ %user_info[3]
    
    smtpserver.sendmail(office365_user, to, msg)
    
    smtpserver.close()     

def navigate(user_info):

    #getting the current day
    CURRENT_DAY = ((((str(datetime.now())).split('-'))[2]).split(' '))[0]

    #if three days have passed and no course was found. Exit the program
    if (int(CURRENT_DAY) - int(START_DAY)) >= 3:

        print('3 days have passed. Course was not found.')
        print('Program will exit now.')
        quit()

    #Creating webdriver object to run on Firefox browser binaries.
    if platform.system() == 'Darwin':

        path_to_firefox = os.path.join(os.path.expanduser('~'),'Applications','Firefox.app','Contents','MacOS','firefox')
        
        import pyvirtualdisplay

        with pyvirtualdisplay.Display(visible=False):

            binary = FirefoxBinary(path_to_firefox)

            driver = webdriver.Firefox(firefox_binary=binary)

    else:

        driver = webdriver.Firefox()

    #Different links to register for spring, summer or fall terms
    if user_info[2] == 'spring':

        driver.get('https://www.isis.ufl.edu/cgi-bin/nirvana?MDASTRAN=RSS-RGCHK2')

    elif user_info[2] == 'summer':

        driver.get('https://www.isis.ufl.edu/cgi-bin/nirvana?MDASTRAN=RSU-RGCHK2')

    elif user_info[2] == 'fall':
      
        driver.get('https://www.isis.ufl.edu/cgi-bin/nirvana?MDASTRAN=RSF-RGCHK2')

    else:

        print('\nThere\'s an error with the information you entered.')
        print('Please re-enter you GatorLink username, password and the term you want to register for.\n')

        del driver

        #if we get here, just close firefox.
        #DOWNSIDE: It will close all firefox instances running on the OS.
        os.system('killall firefox')

        #Go back to asking for user info
        return navigate(getUserInfo())

    time.sleep(1)

    try:    

        assert 'UF Authentication' in driver.title, 'ERROR: Failed to load registration login site'

    except AssertionError:

        print('We apologize, but an error occured while loading the site.')
        print('Plase input your information again.')

        del driver

        return navigate(getUserInfo()) 

    print('\nAuthenticating username and password...')       

    #As soon the isis login website loads, find the input tag whose name is 'j_username'
    username = driver.find_element_by_name('j_username')

    #Pass the username to the username field
    username.send_keys(str(user_info[0]))

    #As soon the isis login website loads, find the input tag whose name is 'j_password'
    password = driver.find_element_by_name('j_password')

    #Pass the password to the password field
    password.send_keys(str(user_info[1]))

    #Press enter (return key)
    password.send_keys(Keys.RETURN)

    time.sleep(1)

    try:

        try:

            #if the username or password are incorrect, an error will occur
            #check if error was generated
            driver.find_element_by_xpath('//p[@class=\'error\']')

            print('\nYour username or password is incorret. Please try again.\n')

            os.system('killall firefox')

            return navigate(getUserInfo())

        except NoSuchElementException:

            pass 

    except NameError:

        pass

    print('Login successful.')               

    #Find the 'Search All Courses' label and click on it
    driver.find_element_by_link_text('Search All Courses').click()

    time.sleep(1)

    #Find the 'Course Number' label and clikc on it
    driver.find_element_by_xpath('//input[@value=\'C\']').click()

    #Find the fiel to input the course number
    course = driver.find_element_by_xpath('//input[@name=\'REGCSE\']')

    #Click on the field to input the course number
    course.click()

    print('Finding course.')

    #Input course number
    course.send_keys(user_info[3])

    #Press enter
    course.send_keys(Keys.RETURN)

    #Find classes in list
    class_list = (driver.find_element_by_id('wellbody').text)

    class_list = unicodedata.normalize('NFKD', class_list).encode('ascii','ignore')

    if(user_info[3].upper() in class_list):

        if CELL_PROVIDED:

            sendText(user_info)
            quit()
        
        else:     
            sendEmail(user_info)
            quit()

    os.system('killall firefox')

    print('Course not found :(\nWill continue running until course is found.')
    print('Maximum running time will be 3 days.')

    time.sleep(350)

    del driver

    navigate(user_info)

def main(args):

    os.system("clear")

    display = Display(visible=0, size=(800, 600))

    display.start()

    global START_DAY 

    #Getting the day that the program started. Will be 3, if the program was started on 11/3
    START_DAY = ((((str(datetime.now())).split('-'))[2]).split(' '))[0]

    global CURRENT_DAY

    try:

        cmd_param = str(args[1])

        if cmd_param == 'install':

            OS = platform.system()

            if OS == 'Darwin':

                os.system('brew install caskroom/cask/brew-cask')

                os.system('brew install Caskroom/cask/firefox')

                os.system('easy_install pip')

                os.system('pip install pyvirtualdisplay selenium')

            elif OS == 'Linux':

                os.system('apt-get install firefox')

                os.system('easy_install pip')

                os.system('pip install pyvirtualdisplay selenium')

            else:

                print('OS not suppoerted. Exiting program now')
                quit()

            os.system('clear')  

        else:
            pass

    except IndexError:
        pass

    navigate(getUserInfo())

if __name__ == '__main__':

    main(sys.argv)
