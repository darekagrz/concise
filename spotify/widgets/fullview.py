from webcore.elements.container import ContainerElement
from selenium.webdriver.common.by import By


class FullView(ContainerElement):

    def __init__(self, locator="NavigationApp-content", by=By.CLASS_NAME):

        ContainerElement.__init__(self, locator, by=by)
