from imagetyperzapi3.imagetyperzapi import ImageTyperzAPI
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from lxml import html



# SETUP CREDENTIALS
IMAGETYPERS_TOKEN = 'toke-id'
FULL_NAME = 'John Davis'
DLNUMBER = 'DLNumber'
BIRTHDAY = '02/16/1982'
PHONE_NUMBER = '415 000 0000'

driver = webdriver.Chrome()

# options = webdriver.ChromeOptions()
# options.add_argument('headless')
#
# driver = webdriver.Chrome(chrome_options=options)

PAGE = 'https://www.dmv.ca.gov/wasapp/foa/driveTest.do'
driver.get(PAGE)

#Which office would you like to visit?

def selectCity(city):
    select = Select(driver.find_element_by_id('officeId'))
    select.select_by_visible_text(city)
    element = driver.find_element_by_xpath("//input[@id='DT']").click()

def custumerInformation(**args):

    for key, value in args.items():
        element = driver.find_element_by_name(f'{key}')
        element.send_keys(value)

    sleep(2) # Let the user actually see something!

    # get sitekey from page
    site_key = driver.find_element_by_class_name('g-recaptcha').get_attribute('data-sitekey')
    data_callback = driver.find_element_by_class_name('g-recaptcha').get_attribute('data-callback')
    print
    '[+] Site key: {}'.format(site_key)
    print
    '[+] Callback method: {}'.format(data_callback)

    driver.find_element_by_xpath("//input[@value='Continue']").click()

    # complete captcha
    print
    '[+] Waiting for recaptcha to be solved ...'
    i = ImageTyperzAPI(IMAGETYPERS_TOKEN)
    recaptcha_params = {
        'page_url': PAGE,
        'sitekey': '6Lc1RGEUAAAAABRCKide8MnHZNTsAuOu4w0VBPwo',
        'type': 2  # invisible
    }
    recaptcha_id = i.submit_recaptcha(recaptcha_params)  # submit recaptcha
    while i.in_progress(recaptcha_id):  # check if still in progress
        sleep(10)  # every 10 seconds
    g_response_code = i.retrieve_recaptcha(recaptcha_id)  # get g-response-code

    print
    '[+] Got g-response-code: {}'.format(g_response_code)  # we got it

    # submit form
    js = '{}("{}");'.format(data_callback, g_response_code)
    driver.execute_script(js)


selectCity('SAN FRANCISCO')

name = FULL_NAME.split(' ')
custumerInformation(firstName=name[0],lastName=name[1], dlNumber=DLNUMBER, birthMonth=BIRTHDAY[0:3],
                    birthDay=BIRTHDAY[3:], birthYear=BIRTHDAY[6:10], telArea=PHONE_NUMBER[0:3], telPrefix=PHONE_NUMBER[4:7], telSuffix=PHONE_NUMBER[8:])


print(driver.current_url)
#driver.quit()