from zope.component import getUtility, getMultiAdapter

from plone.portlets.interfaces import IPortletType
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletRenderer

from plone.app.portlets.storage import PortletAssignmentMapping

from collective.portlet.actions import actionsportlet

from collective.portlet.actions.tests.base import TestCase


class TestPortlet(TestCase):

    def afterSetUp(self):
        self.setRoles(('Manager', ))
        return

    def test_portlet_type_registered(self):
        portlet = getUtility(
            IPortletType,
            name='collective.portlet.actions.ActionsPortlet')
        self.assertEquals(portlet.addview,
                          'collective.portlet.actions.ActionsPortlet')
        return

    def test_interfaces(self):
        portlet = actionsportlet.Assignment(title=u'actions', category=u'document', show_icons=True)
        self.failUnless(IPortletAssignment.providedBy(portlet))
        self.failUnless(IPortletDataProvider.providedBy(portlet.data))
        return

    def test_invoke_add_view(self):
        portlet = getUtility(
            IPortletType,
            name='collective.portlet.actions.ActionsPortlet')
        mapping = self.portal.restrictedTraverse(
            '++contextportlets++plone.leftcolumn')
        for m in mapping.keys():
            del mapping[m]
        addview = mapping.restrictedTraverse('+/' + portlet.addview)

        data = {
            'title': u"Actions",
            'category': u'document',
            'show_icons': True}
        addview.createAndAdd(data=data)

        self.assertEquals(len(mapping), 1)
        self.failUnless(isinstance(mapping.values()[0],
                                   actionsportlet.Assignment))
        return

    def test_invoke_edit_view(self):
        mapping = PortletAssignmentMapping()
        request = self.folder.REQUEST

        mapping['foo'] = actionsportlet.Assignment(title=u'actions', category=u'document', show_icons=True)
        editview = getMultiAdapter((mapping['foo'], request), name='edit')
        self.failUnless(isinstance(editview, actionsportlet.EditForm))
        return

    def test_obtain_renderer(self):
        context = self.folder
        request = self.folder.REQUEST
        view = self.folder.restrictedTraverse('@@plone')
        manager = getUtility(IPortletManager, name='plone.rightcolumn',
                             context=self.portal)

        assignment = actionsportlet.Assignment(title=u'actions', category=u'document', show_icons=True)

        renderer = getMultiAdapter(
            (context, request, view, manager, assignment), IPortletRenderer)
        self.failUnless(isinstance(renderer, actionsportlet.Renderer))
        return


class TestRenderer(TestCase):

    def afterSetUp(self):
        self.setRoles(('Manager', ))
        return

    def renderer(self, context=None, request=None, view=None, manager=None,
                 assignment=None):
        context = context or self.folder
        request = request or self.folder.REQUEST
        view = view or self.folder.restrictedTraverse('@@plone')
        manager = manager or getUtility(
            IPortletManager, name='plone.rightcolumn', context=self.portal)

        assignment = assignment or actionsportlet.Assignment(title=u'actions', category=u'site_actions', show_icons=True)
        return getMultiAdapter((context, request, view, manager, assignment),
                               IPortletRenderer)

    def test_render(self):
        r = self.renderer(context=self.portal,
                          assignment=actionsportlet.Assignment(title=u'actions', category=u'site_actions', show_icons=True))
        r = r.__of__(self.folder)
        r.update()
        output = r.actionLinks()
        self.failUnlessEqual(len(output), 4)

        first = output[0]
        self.failUnlessEqual(first['url'], 'http://nohost/plone/sitemap')
        self.failUnless(first['icon'] is not None, "We should have an icon")
        self.failUnlessEqual(first['title'], u"Site Map")
        return

    def test_render_woicon(self):
        """Without icons"""
        r = self.renderer(context=self.portal,
                          assignment=actionsportlet.Assignment(title=u'actions', category=u'site_actions', show_icons=False))
        r = r.__of__(self.folder)
        r.update()
        output = r.actionLinks()
        first = output[0]
        self.failUnless(first['icon'] is None, "We should not have an icon")
        return


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPortlet))
    suite.addTest(makeSuite(TestRenderer))
    return suite
