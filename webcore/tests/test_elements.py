import logging
import datetime

import pytest

from webcore.wdcore_driver import WdCoreDriver
from webcore.tests.page_objects import HomePage, CheckboxesPage, DropdownPage, JavaScriptAlertsPage, BrokenImagesPage, \
    DisappearingElementsPage, DragAndDropPage, NestedFramesPage, DataTablesPage


@pytest.fixture
def generate_driver(request):
    """ A fixture to startup the webdriver and navigate to the test site before every test. """
    console_formatter = '[%(levelname)s] %(name)s %(message)s'
    logging.basicConfig(level=logging.NOTSET, format=console_formatter)

    driver = WdCoreDriver(url='http://the-internet.herokuapp.com/')

    def final():
        """ Close driver at completion of test """
        driver.driver.quit()
    request.addfinalizer(final)

    return driver


def test_broken_images(generate_driver):

    # Create an instance of the home page to work with.
    home_page = HomePage()
    home_page.click_link('Broken Images')

    # Create an instance of the example page and verify the header
    page = BrokenImagesPage()
    assert page.header.text() == 'Broken Images'

    #Verify images 1 and 2 are broken
    assert page.image_1.attribute('naturalWidth') == '0'
    assert page.image_1.attribute('naturalHeight') == '0'

    assert page.image_2.attribute('naturalWidth') == '0'
    assert page.image_2.attribute('naturalHeight') == '0'

    assert page.image_3.attribute('naturalWidth') != '0'
    assert page.image_3.attribute('naturalHeight') != '0'


def test_checkbox_element(generate_driver):

    # Create an instance of the home page to work with.
    home_page = HomePage()
    home_page.click_link('Checkboxes')

    # Create an instance of the example page and verify the header
    page = CheckboxesPage()
    assert page.header.text() == 'Checkboxes'

    # Check checkbox 1 and uncheck checkbox 2. Verify that was successful
    page.checkbox_1.value(True)
    page.checkbox_2.value(False)
    assert page.checkbox_1.value() is True
    assert page.checkbox_2.value() is False


def test_disappearing_elements(generate_driver):

    # Create an instance of the home page to work with.
    home_page = HomePage()
    home_page.click_link('Disappearing Elements')

    # Create an instance of the example page and verify the header
    page = DisappearingElementsPage()
    assert page.header.text() == 'Disappearing Elements'

    assert page.button(1).text() == 'Home'
    assert page.button(2).text() == 'About'
    assert page.button(3).text() == 'Contact Us'
    assert page.button(4).text() == 'Portfolio'

    if page.buttons.count() == 4:
        assert page.button(5).exists() is False
    else:
        assert page.button(5).text() == 'Gallery'


@pytest.mark.xfail(run=False, reason="Test fails because drag and drop doesn't work on test page.")
def test_drag_and_drop(generate_driver):

    # Create an instance of the home page to work with.
    home_page = HomePage()
    home_page.click_link('Drag and Drop')

    # Create an instance of the example page and verify the header
    page = DragAndDropPage()
    assert page.header.text() == 'Drag and Drop'

    assert page.column_a_box.text() == 'A'
    assert page.column_b_box.text() == 'B'

    page.column_a_box.drag_to(destination=page.column_b_box)

    # TODO - test fails because drag and drop doesn't appear to function on test page.


def test_dropdown_element(generate_driver):

    # Create an instance of the home page to work with.
    home_page = HomePage()
    home_page.click_link('Dropdown')

    # Create an instance of the example page and verify the header
    page = DropdownPage()
    assert page.header.text() == 'Dropdown List'

    # Verify dropdown can be set by the text of the option
    page.dropdown.set('Option 1')
    assert page.dropdown.text() == 'Option 1'
    assert page.dropdown.value() == '1'

    # Verify dropdown can be set by value of the option
    page.dropdown.value(2)
    assert page.dropdown.text() == 'Option 2'
    assert page.dropdown.value() == '2'


def test_javascript_alerts(generate_driver):

    # Create an instance of the home page to work with.
    home_page = HomePage()
    home_page.click_link('JavaScript Alerts')

    # Create an instance of the example page and verify the header
    page = JavaScriptAlertsPage()
    assert page.header.text() == 'JavaScript Alerts'

    # Verify dropdown can be set by the text of the option
    page.js_alert_button.click()
    page.alert.accept()
    assert page.result.text() == 'You successfuly clicked an alert'

    page.js_confirm_button.click()
    assert page.alert.text == 'I am a JS Confirm'
    page.alert.accept()
    assert page.result.text() == 'You clicked: Ok'

    page.js_confirm_button.click()
    page.alert.dismiss()
    assert page.result.text() == 'You clicked: Cancel'


def test_nested_frames(generate_driver):

    # Create an instance of the home page to work with.
    home_page = HomePage()
    home_page.click_link('Nested Frames')

    # Create an instance of the example page and verify the header
    page = NestedFramesPage()

    assert page.left_body.text().strip() == 'LEFT'
    assert page.right_body.text().strip() == 'RIGHT'
    assert page.bottom_body.text().strip() == 'BOTTOM'
    assert page.middle_body.text().strip() == 'MIDDLE'


def test_data_tables(generate_driver):

    # Create an instance of the home page to work with.
    home_page = HomePage()
    home_page.click_link('Sortable Data Tables')

    # Create an instance of the example page and verify the header
    page = DataTablesPage()
    assert page.header.text() == 'Data Tables'

    assert page.table1.header_cell(column=1).text() == 'Last Name'
    assert page.table1.header_cell(column=2).text() == 'First Name'
    assert page.table1.header_cell(column=3).text() == 'Email'
    assert page.table1.header_cell(column=4).text() == 'Due'
    assert page.table1.header_cell(column=5).text() == 'Web Site'
    assert page.table1.header_cell(column=6).text() == 'Action'

    assert page.table1.body_cell(row=1, column=1).text() == 'Smith'
    assert page.table1.body_cell(row=1, column=2).text() == 'John'
    assert page.table1.body_cell(row=2, column=3).text() == 'fbach@yahoo.com'
    assert page.table1.body_cell(row=2, column=4).text() == '$51.00'
    assert page.table1.body_cell(row=3, column=5).text() == 'http://www.jdoe.com'
    assert 'edit' in page.table1.body_cell(row=3, column=6).text()
    assert 'delete' in page.table1.body_cell(row=3, column=6).text()
