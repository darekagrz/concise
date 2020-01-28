from selenium.webdriver.common.by import By
from webcore.elements.frame import FrameElement
from webcore.elements.input import CheckboxElement, SelectElement
from webcore.elements.table import TableElement

from webcore.pages.page import Page
from webcore.elements.display import DisplayElement


class HomePage(Page):
    """Home page action methods come here. I.e. Python.org"""

    # region ---------- Page Objects Here ----------

    header = DisplayElement('//div[@id="content"]/h1', By.XPATH)
    sub_header = DisplayElement('//div[@id="content"]/h2', By.XPATH)

    # endregion

    @staticmethod
    def click_link(link_text):
        """Triggers the search"""
        element = DisplayElement(link_text, By.LINK_TEXT).get_element()
        element.click()


class ExamplePage(Page):

    header = DisplayElement('#content>div>h3', By.CSS_SELECTOR)


class CheckboxesPage(ExamplePage):
    
    # region ---------- Page Objects Here ----------

    checkbox_1 = CheckboxElement('//form[@id="checkboxes"]/input[1]', By.XPATH)
    checkbox_2 = CheckboxElement('//form[@id="checkboxes"]/input[2]', By.XPATH)

    # endregion


class DropdownPage(ExamplePage):

    # region ---------- Page Objects Here ----------

    dropdown = SelectElement('dropdown', By.ID)

    # endregion


class JavaScriptAlertsPage(ExamplePage):

    # region ---------- Page Objects Here ----------

    js_alert_button = DisplayElement('//button[.="Click for JS Alert"]', By.XPATH)
    js_confirm_button = DisplayElement('//button[.="Click for JS Confirm"]', By.XPATH)
    js_prompt_button = DisplayElement('//button[.="Click for JS Prompt"]', By.XPATH)
    result = DisplayElement('result', By.ID)

    # endregion


class BrokenImagesPage(ExamplePage):

    image_container = DisplayElement('div.example', By.CSS_SELECTOR)
    image_1 = DisplayElement('/img[1]', By.XPATH, parent=image_container)
    image_2 = DisplayElement('/img[2]', By.XPATH, parent=image_container)
    image_3 = DisplayElement('/img[3]', By.XPATH, parent=image_container)


class DisappearingElementsPage(ExamplePage):

    button_list = DisplayElement('div.example>ul', By.CSS_SELECTOR)
    buttons = DisplayElement('/li', By.XPATH, parent=button_list)

    def button(self, button_num):
        return DisplayElement('/li[{0}]'.format(button_num), By.XPATH, parent=self.button_list)


class DragAndDropPage(ExamplePage):

    column_a_box = DisplayElement('column-a', By.ID)
    column_b_box = DisplayElement('column-b', By.ID)


class TopFrame(FrameElement):

    def __init__(self):
        FrameElement.__init__(self, 'frame-top', by=By.NAME)

    left_frame = FrameElement('frame-left', by=By.NAME)
    middle_frame = FrameElement('frame-middle', by=By.NAME)


class NestedFramesPage(ExamplePage):

    top_frame = TopFrame()
    left_frame = top_frame.left_frame
    middle_frame = top_frame.middle_frame

    right_frame = FrameElement('frame-right', by=By.NAME)

    top_frame.add_children(right_frame)

    bottom_frame = FrameElement('frame-bottom', by=By.NAME)

    left_body = DisplayElement('body', By.TAG_NAME, left_frame)
    middle_body = DisplayElement('//body', By.XPATH, middle_frame)
    right_body = DisplayElement('body', By.TAG_NAME, right_frame)
    bottom_body = DisplayElement('body', By.TAG_NAME, bottom_frame)


class DataTablesPage(ExamplePage):

    table1 = TableElement('table1', By.ID)
    table2 = TableElement('table2', By.ID)
