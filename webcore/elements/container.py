import logging

from webcore.elements.element import Element

LOGGER = logging.getLogger(__name__)


class ContainerElement(Element):
    """
    An Element object that contains other elements.
    This Element simply handles the addition of any other Element object that is a component of the Container as
    a child of the Container element.
    """

    def __init__(self, locator, by=None, parent=None):
        Element.__init__(self, locator, by, parent)
        self.add_all_element_instance_variables_as_children()
