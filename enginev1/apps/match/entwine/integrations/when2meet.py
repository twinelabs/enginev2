"""
integrations.when2meet
--------

when2meet creation
TODO: wrap in Python
"""

n = 11

for i in range(n):

    path_to_chromedriver = '/Users/ns/Downloads/chromedriver'
    browser = webdriver.Chrome(executable_path = path_to_chromedriver)
    browser.get('http://www.when2meet.com')

    # Name Event
    event_name = 'LF Meetup'
    event_name_input = browser.find_element_by_id('NewEventName')
    event_name_input.clear()
    event_name_input.send_keys(event_name)

    # Select Days
    days_selected = ['Day-1-7', 'Day-2-1', 'Day-2-2', 'Day-2-3', 'Day-2-4', 'Day-2-5', 'Day-2-6', 'Day-2-7']
    for d in days_selected:
        day_elem = browser.find_element_by_id(d)
        day_elem.click()

    # Select Times
    start_elem = browser.find_element_by_xpath("//select[@name='NoEarlierThan']/option[@value='16']")
    start_elem.click()

    end_elem  = browser.find_element_by_xpath("//select[@name='NoLaterThan']/option[@value='23']")
    end_elem.click()

    # Create Event
    xyz = browser.find_element_by_xpath('//input[@type="submit" and @value="Create Event"]')
    xyz.click()

    print browser.current_url

    browser.quit()

