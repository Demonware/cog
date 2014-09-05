import sys
import unittest

sys.path.append("../cog")

from cog import directory
from cog.config import Profiles
from mock import patch, Mock
from random import randint

settings = Profiles().current()
min_uidnumber = settings.get('min_uidnumber')
max_uidnumber = settings.get('max_uidnumber')
min_gidnumber = settings.get('min_gidnumber')
max_gidnumber = settings.get('max_gidnumber')
test_uidnumber = randint(min_uidnumber, max_uidnumber)
test_gidnumber = randint(min_gidnumber, max_gidnumber)


class TestDirectory(unittest.TestCase):

    @patch.object(directory.Tree, 'search', new=Mock())
    def test__get_probably_unique_uidnumber__succeeds(self):
        directory.Tree.search.return_value = [
            {'uidNumber': [str(test_uidnumber)]},
            {'uidNumber': [str(randint(min_uidnumber, test_uidnumber - 1))]},
            {'uidNumber': [str(randint(min_uidnumber, test_uidnumber - 1))]}]
        uid = directory.get_probably_unique_uidnumber()
        self.assertEqual(uid, str(test_uidnumber + 1))

    @patch.object(directory.Tree, 'search', new=Mock())
    def test__get_probably_unique_uidnumber__no_uids__succeeds(self):
        directory.Tree.search.return_value = []
        uid = directory.get_probably_unique_uidnumber()
        self.assertEqual(uid, str(min_uidnumber + 1))

    @patch.object(directory.Tree, 'search', new=Mock())
    def test__get_probably_unique_gidnumber__succeeds(self):
        directory.Tree.search.return_value = [
            {'gidNumber': [str(test_gidnumber)]},
            {'gidNumber': [str(randint(min_gidnumber, test_gidnumber - 1))]},
            {'gidNumber': [str(randint(min_gidnumber, test_gidnumber - 1))]}]
        gid = directory.get_probably_unique_gidnumber()
        self.assertEqual(gid, str(test_gidnumber + 1))

    @patch.object(directory.Tree, 'search', new=Mock())
    def test__get_probably_unique_gidnumber__no_gids__succeeds(self):
        directory.Tree.search.return_value = []
        gid = directory.get_probably_unique_gidnumber()
        self.assertEqual(gid, str(min_gidnumber + 1))

