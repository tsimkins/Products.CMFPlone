# -*- coding: utf-8 -*-
from Products.CMFPlone.testing import PRODUCTS_CMFPLONE_FUNCTIONAL_TESTING
from plone.app.testing import SITE_OWNER_NAME, SITE_OWNER_PASSWORD
from plone.testing.z2 import Browser
import unittest2 as unittest


class TypesControlPanelFunctionalTest(unittest.TestCase):
    """Test that changes in the types control panel are actually
    stored in the registry.
    """

    layer = PRODUCTS_CMFPLONE_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.portal_url = self.portal.absolute_url()
        self.types_url = "%s/@@types-controlpanel" % self.portal_url
        self.browser = Browser(self.app)
        self.browser.handleErrors = False
        self.browser.addHeader(
            'Authorization',
            'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD,)
        )

    def test_types_control_panel_link(self):
        self.browser.open(
            "%s/plone_control_panel" % self.portal_url)
        self.browser.getLink('Editing').click()

    def test_standard_type_select(self):
        self.browser.open(self.types_url)
        self.browser.getControl(name='type_id').value = ['Link']
        self.browser.getForm(action=self.types_url).submit()
        self.assertIn('types-controlpanel', self.browser.url)

    def test_standard_type_cancel(self):
        self.browser.open(self.types_url)
        self.browser.getControl(name='type_id').value = ['Link']
        self.browser.getControl('Cancel').click()
        self.assertIn('plone_control_panel', self.browser.url)

    def test_standard_type_allow_commenting(self):
        self.browser.open(self.types_url)
        self.browser.getControl(name='type_id').value = ['Link']
        self.browser.getForm(action=self.types_url).submit()
        self.browser.getControl('Allow comments').selected = True
        self.browser.getControl('Apply Changes').click()

        # Check if settings got saved correctly
        self.browser.open(self.types_url)
        self.browser.getControl(name='type_id').value = ['Link']
        self.browser.getForm(action=self.types_url).submit()
        self.assertIn('Globally addable', self.browser.contents)
        self.assertIn('Allow comments', self.browser.contents)
        self.assertEquals(
            self.browser.getControl('Allow comments').selected,
            True
        )
        self.assertIn('Visible in searches', self.browser.contents)
        self.assertIn(
            '<input id="redirect_links" type="checkbox" class="noborder"'
            ' name="redirect_links:boolean" checked="checked" />',
            self.browser.contents)
        self.assertIn(
            '<label for="redirect_links">Redirect immediately to link target',
            self.browser.contents
        )

    def test_set_no_default_workflow(self):
        # references http://dev.plone.org/plone/ticket/11901
        self.browser.open(self.types_url)
        self.browser.getControl(name="new_workflow").value = ['[none]']
        self.browser.getControl(name="form.button.Save").click()

        # Check that setting No workflow as default workflow doesn't break
        # break editing types
        self.browser.open(self.types_url)
        self.browser.getControl(name='type_id').value = ['Link']
        self.browser.getForm(action=self.types_url).submit()
        self.assertIn('Globally addable', self.browser.contents)
        self.assertIn('Allow comments', self.browser.contents)
        self.assertIn('Visible in searches', self.browser.contents)