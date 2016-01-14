#
# stdlib
#
import os
import unittest
#
# jsonstat
#
import jsonstat
import jsonstat.istat as istat


class TestIstat(unittest.TestCase):
    def setUp(self):
        self.fixture_dir = os.path.join(os.path.dirname(__file__), "fixtures", "istat")

    def test_istat_italian(self):
        i = istat.Istat(self.fixture_dir, lang=0)
        n = i.area(26).name()
        self.assertEqual("Lavoro", n)

        d = i.area(26).dataset('DCCV_INATTIVMENS').name()
        self.assertEqual(u'Inattivi - dati mensili', d)

        # name = i.area(26).datasets('DCCV_INATTIVMENS').dimensions(0).name()

    def test_istat_english(self):
        i = istat.Istat(self.fixture_dir, lang=1)
        n = i.area(26).name()
        self.assertEqual("Labour", n)

        d = i.area(26).dataset('DCCV_INATTIVMENS').name()
        self.assertEqual(u'Inactive population - monthly data', d)

        dim = i.area(26).dataset('DCCV_INATTIVMENS').dimension(0)
        self.assertEqual('Territory', dim.name())


if __name__ == '__main__':
    unittest.main()