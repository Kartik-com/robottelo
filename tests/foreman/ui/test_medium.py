# -*- encoding: utf-8 -*-
# vim: ts=4 sw=4 expandtab ai
"""Test class for Medium UI"""

from ddt import ddt
from fauxfactory import FauxFactory
from robottelo import entities
from robottelo.common.constants import INSTALL_MEDIUM_URL
from robottelo.common.decorators import data, run_only_on
from robottelo.common.helpers import generate_strings_list
from robottelo.test import UITestCase
from robottelo.ui.factory import make_media
from robottelo.ui.locators import common_locators
from robottelo.ui.session import Session


@run_only_on('sat')
@ddt
class Medium(UITestCase):
    """Implements all Installation Media tests"""

    org_name = None
    loc_name = None
    org_id = None
    loc_id = None

    def setUp(self):
        super(Medium, self).setUp()
        #  Make sure to use the Class' org_name instance
        if (Medium.org_name is None and Medium.loc_name is None):
            org_name = FauxFactory.generate_string("alpha", 8)
            loc_name = FauxFactory.generate_string("alpha", 8)
            org_attrs = entities.Organization(name=org_name).create()
            loc_attrs = entities.Location(name=loc_name).create()
            Medium.org_name = org_attrs['name']
            Medium.org_id = org_attrs['id']
            Medium.loc_name = loc_attrs['name']
            Medium.loc_id = loc_attrs['id']

    @data(*generate_strings_list(len1=4))
    def test_positive_create_medium_1(self, name):
        """@Test: Create a new media

        @Feature:  Media - Positive Create

        @Assert: Media is created

        """

        path = INSTALL_MEDIUM_URL % FauxFactory.generate_string("alpha", 6)
        os_family = "Red Hat"
        with Session(self.browser) as session:
            make_media(session, name=name, path=path, os_family=os_family)
            self.assertIsNotNone(self.medium.search(name))

    @data(
        FauxFactory.generate_string('alphanumeric', 255),
        FauxFactory.generate_string('alpha', 255),
        FauxFactory.generate_string('numeric', 255),
        FauxFactory.generate_string('latin1', 255),
        FauxFactory.generate_string('utf8', 255)
    )
    def test_positive_create_medium_2(self, name):
        """@Test: Create a new media with 255 characters in name

        @Feature:  Media - Positive Create

        @Assert: Media is created

        """

        path = INSTALL_MEDIUM_URL % FauxFactory.generate_string("alpha", 6)
        os_family = "Red Hat"
        with Session(self.browser) as session:
            make_media(session, name=name,
                       path=path, os_family=os_family)
            self.assertIsNotNone(self.medium.search(name))

    def test_negative_create_medium_1(self):
        """@Test: Create a new install media with 256 characters in name

        @Feature:  Media - Negative Create

        @Assert: Media is not created

        """

        name = FauxFactory.generate_string("alpha", 256)
        path = INSTALL_MEDIUM_URL % name
        os_family = "Red Hat"
        with Session(self.browser) as session:
            make_media(session, name=name, path=path, os_family=os_family)
            self.assertIsNotNone(self.medium.wait_until_element
                                 (common_locators["name_haserror"]))
            self.assertIsNone(self.medium.search(name))

    @data("", "  ")
    def test_negative_create_medium_2(self, name):
        """@Test: Create a new install media with blank and whitespace in name

        @Feature:  Media - Negative Create

        @Assert: Media is not created

        """

        path = INSTALL_MEDIUM_URL % FauxFactory.generate_string("alpha", 6)
        os_family = "Red Hat"
        with Session(self.browser) as session:
            make_media(session, name=name, path=path, os_family=os_family)
            self.assertIsNotNone(self.medium.wait_until_element
                                 (common_locators["name_haserror"]))

    def test_negative_create_medium_4(self):
        """@Test: Create a new install media with same name

        @Feature:  Media - Negative Create

        @Assert: Media is not created

        """

        name = FauxFactory.generate_string("alpha", 6)
        path = INSTALL_MEDIUM_URL % name
        os_family = "Red Hat"
        with Session(self.browser) as session:
            make_media(session, name=name, path=path, os_family=os_family)
            self.assertIsNotNone(self.medium.search(name))
            make_media(session, name=name, path=path, os_family=os_family)
            self.assertIsNotNone(self.medium.wait_until_element
                                 (common_locators["name_haserror"]))

    def test_negative_create_medium_5(self):
        """@Test: Create a new install media without media URL

        @Feature:  Media - Negative Create

        @Assert: Media is not created

        """

        name = FauxFactory.generate_string("alpha", 6)
        path = ""
        os_family = "Red Hat"
        with Session(self.browser) as session:
            make_media(session, name=name, path=path, os_family=os_family)
            self.assertIsNotNone(self.medium.wait_until_element
                                 (common_locators["haserror"]))
            self.assertIsNone(self.medium.search(name))

    def test_negative_create_medium_6(self):
        """@Test: Create an install media with an existing URL

        @Feature:  Media - Negative Create

        @Assert: Media is not created

        """

        name = FauxFactory.generate_string("alpha", 6)
        new_name = FauxFactory.generate_string("alpha", 6)
        path = INSTALL_MEDIUM_URL % FauxFactory.generate_string("alpha", 6)
        os_family = "Red Hat"
        with Session(self.browser) as session:
            make_media(session, name=name, path=path, os_family=os_family)
            self.assertIsNotNone(self.medium.search(name))
            make_media(session, name=new_name, path=path, os_family=os_family)
            self.assertIsNotNone(self.medium.wait_until_element
                                 (common_locators["haserror"]))
            self.assertIsNone(self.medium.search(new_name))

    def test_remove_medium(self):
        """@Test: Delete a media

        @Feature: Media - Delete

        @Assert: Media is deleted

        """
        name = FauxFactory.generate_string("alpha", 6)
        path = INSTALL_MEDIUM_URL % name
        os_family = "Red Hat"
        with Session(self.browser) as session:
            make_media(session, name=name, path=path, os_family=os_family)
            self.assertIsNotNone(self.medium.search(name))
            self.medium.delete(name, True)
            self.assertIsNotNone(self.medium.wait_until_element
                                 (common_locators["notif.success"]))
            self.assertIsNone(self.medium.search(name))

    def test_update_medium(self):
        """@Test: Updates Install media with name, path, OS family

        @Feature: Media - Update

        @Assert: Media is updated

        """
        name = FauxFactory.generate_string("alpha", 6)
        newname = FauxFactory.generate_string("alpha", 4)
        path = INSTALL_MEDIUM_URL % name
        newpath = INSTALL_MEDIUM_URL % newname
        os_family = "Red Hat"
        new_os_family = "Debian"
        with Session(self.browser) as session:
            make_media(session, name=name, path=path, os_family=os_family)
            self.assertIsNotNone(self.medium.search(name))
            self.medium.update(name, newname, newpath, new_os_family)
            self.assertTrue(self, self.medium.search(newname))
