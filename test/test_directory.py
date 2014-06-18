import sys
import unittest

sys.path.append("../cog")

from cog import directory
from mock import patch, Mock


class TestDirectory(unittest.TestCase):
    
    @patch.object(directory.Tree, 'search', new=Mock())
    def test__get_probably_unique_uidnumber__succeeds(self):
        directory.Tree.search.return_value = [ 
            {'uidNumber': ['88888']},
            {'uidNumber': ['8']},
            {'uidNumber': ['600']}]
        uid = directory.get_probably_unique_uidnumber()
        self.assertEqual(uid, '88889')

    @patch.object(directory.Tree, 'search', new=Mock())
    def test__get_probably_unique_uidnumber__no_uids__succeeds(self):
        directory.Tree.search.return_value = []
        uid = directory.get_probably_unique_uidnumber()
        self.assertEqual(uid, '1')

    @patch.object(directory.Tree, 'search', new=Mock())
    def test__get_probably_unique_gidnumber__succeeds(self):
        directory.Tree.search.return_value = [ 
            {'gidNumber': ['88888']},
            {'gidNumber': ['8']},
            {'gidNumber': ['600']}]
        gid = directory.get_probably_unique_gidnumber()
        self.assertEqual(gid, '88889')

    @patch.object(directory.Tree, 'search', new=Mock())
    def test__get_probably_unique_gidnumber__no_gids__succeeds(self):
        directory.Tree.search.return_value = []
        gid = directory.get_probably_unique_gidnumber()
        self.assertEqual(gid, '9201')

