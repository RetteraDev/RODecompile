#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\tzlocal/tests.o
import sys
import os
from datetime import datetime
import unittest
import pytz
import tzlocal.unix
import tzlocal.darwin

class TzLocalTests(unittest.TestCase):

    def setUp(self):
        if 'TZ' in os.environ:
            del os.environ['TZ']
        self.path = os.path.split(__file__)[0]

    def test_env(self):
        tz_harare = tzlocal.unix._tz_from_env(':Africa/Harare')
        self.assertEqual(tz_harare.zone, 'Africa/Harare')
        tz_harare = tzlocal.unix._tz_from_env('Africa/Harare')
        self.assertEqual(tz_harare.zone, 'Africa/Harare')
        tz_local = tzlocal.unix._tz_from_env(':' + os.path.join(self.path, 'test_data', 'Harare'))
        self.assertEqual(tz_local.zone, 'local')
        dt = datetime(2012, 1, 1, 5)
        self.assertEqual(tz_harare.localize(dt), tz_local.localize(dt))
        self.assertRaises(pytz.UnknownTimeZoneError, tzlocal.unix._tz_from_env, 'GMT+03:00')

    def test_timezone(self):
        tz = tzlocal.unix._get_localzone(_root=os.path.join(self.path, 'test_data', 'timezone'))
        self.assertEqual(tz.zone, 'Africa/Harare')

    def test_zone_setting(self):
        tz = tzlocal.unix._get_localzone(_root=os.path.join(self.path, 'test_data', 'zone_setting'))
        self.assertEqual(tz.zone, 'Africa/Harare')

    def test_timezone_setting(self):
        tz = tzlocal.unix._get_localzone(_root=os.path.join(self.path, 'test_data', 'timezone_setting'))
        self.assertEqual(tz.zone, 'Africa/Harare')

    def test_symlink_localtime(self):
        tz = tzlocal.unix._get_localzone(_root=os.path.join(self.path, 'test_data', 'symlink_localtime'))
        self.assertEqual(tz.zone, 'Africa/Harare')

    def test_vardbzoneinfo_setting(self):
        tz = tzlocal.unix._get_localzone(_root=os.path.join(self.path, 'test_data', 'vardbzoneinfo'))
        self.assertEqual(tz.zone, 'Africa/Harare')

    def test_only_localtime(self):
        tz = tzlocal.unix._get_localzone(_root=os.path.join(self.path, 'test_data', 'localtime'))
        self.assertEqual(tz.zone, 'local')
        dt = datetime(2012, 1, 1, 5)
        self.assertEqual(pytz.timezone('Africa/Harare').localize(dt), tz.localize(dt))

    def test_darwin(self):
        tz = tzlocal.darwin._get_localzone(_root=os.path.join(self.path, 'test_data', 'symlink_localtime'))
        self.assertEqual(tz.zone, 'Africa/Harare')


if sys.platform == 'win32':
    import tzlocal.win32

    class TzWin32Tests(unittest.TestCase):

        def test_win32(self):
            tzlocal.win32.get_localzone()


if __name__ == '__main__':
    unittest.main()
