import unittest
import mock
from StringIO import StringIO as IO
from httpdb import myHandler, HTTPServer




class MockRequest(object):
    def __init__(self, request):
        self.request = request

    def makefile(self, *args, **kwargs):
        return IO(self.request)




class HttpDBTest(unittest.TestCase):

    def setUp(self):
        self.test_request = MockRequest(b"GET / HTTP/1.1")


    @mock.patch("httpdb.HTTPServer")
    def test_get_validate_path(self, mock_server):
        test_handler = myHandler(self.test_request, ("",4000), mock_server)

        path, key, value = test_handler.validate_path("/get?key=a")
        self.assertEquals(path, "/get")
        self.assertEquals(key, "key")
        self.assertEquals(value, "a")

        path, key, value = test_handler.validate_path("/get?key=1")
        self.assertEquals(path, "/get")
        self.assertEquals(key, "key")
        self.assertEquals(value, "1")

        path, key, value = test_handler.validate_path("/get?key=!$%%^$THDT")
        self.assertEquals(path, "/get")
        self.assertEquals(key, "key")
        self.assertEquals(value, "!$%%^$THDT")

        self.assertRaises(ValueError, test_handler.validate_path, "/get?key=1&key=2")
        self.assertRaises(ValueError, test_handler.validate_path, "/get?somekey=1&somekey=2")
        self.assertRaises(ValueError, test_handler.validate_path, "/get?key!$%%^$THDT")




    @mock.patch("httpdb.HTTPServer")
    def test_set_validate_path(self, mock_server):
        test_handler = myHandler(self.test_request, ("",4000), mock_server)

        path, key, value = test_handler.validate_path("/set?somekey=a")
        self.assertEquals(path, "/set")
        self.assertEquals(key, "somekey")
        self.assertEquals(value, "a")

        path, key, value = test_handler.validate_path("/set?somekey=1")
        self.assertEquals(path, "/set")
        self.assertEquals(key, "somekey")
        self.assertEquals(value, "1")

        path, key, value = test_handler.validate_path("/set?somekey=!$%%^$THDT")
        self.assertEquals(path, "/set")
        self.assertEquals(key, "somekey")
        self.assertEquals(value, "!$%%^$THDT")

        self.assertRaises(ValueError, test_handler.validate_path, "/set?key=1&key=2")
        self.assertRaises(ValueError, test_handler.validate_path, "/set?somekey=1&somekey=2")
        self.assertRaises(ValueError, test_handler.validate_path, "/set?somekey!$%%^$THDT")




    @mock.patch("httpdb.HTTPServer")
    def test_set_value(self, mock_server):
        test_handler = myHandler(self.test_request, ("",4000), mock_server)

        test_handler.set_value("somekey","a")
        self.assertEquals(test_handler.myDB["somekey"],"a")
        test_handler.set_value("somekey","1")
        self.assertEquals(test_handler.myDB["somekey"],"1")
        test_handler.set_value("somekey", 1)
        self.assertEquals(test_handler.myDB["somekey"], 1)
        test_handler.set_value("anotherkey", "a")
        self.assertEquals(test_handler.myDB["anotherkey"], "a")




    @mock.patch("httpdb.HTTPServer")
    def test_get_value(self, mock_server):
        test_handler = myHandler(self.test_request, ("",4000), mock_server)

        test_handler.set_value("somekey","a")
        self.assertEquals(test_handler.get_value("key","somekey"), "a")

        test_handler.set_value("anotherkey", 1)
        self.assertEquals(test_handler.get_value("key","anotherkey"), 1)

        self.assertRaises(ValueError, test_handler.get_value, "notkey", "somekey")



if __name__ == '__main__':
    unittest.main()
