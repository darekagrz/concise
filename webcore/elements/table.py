
from selenium.webdriver.common.by import By
from webcore.elements.display import DisplayElement
from webcore.elements.element import Element

import logging

LOGGER = logging.getLogger(__name__)


class TableElement(Element):

    def header_cell(self, row=1, column=1):
        return DisplayElement('/thead/tr[{row}]/th[{column}]'.format(row=row, column=column), By.XPATH, self)

    def body_row(self, row=1):
        return DisplayElement('/tbody/tr[{row}]'.format(row=row), By.XPATH, self)

    def body_cell(self, row=1, column=1):
        return DisplayElement('/tbody/tr[{row}]/td[{column}]'.format(row=row, column=column), By.XPATH, self)

    @property
    def row_count(self):
        return len(self.get_element().find_elements_by_tag_name('tr'))
