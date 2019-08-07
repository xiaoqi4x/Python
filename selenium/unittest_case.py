import unittest
class FirstCase01(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("this is all case precondition")

    @classmethod
    def tearDownClass(cls):
        print("this is all case post condition")

    def setUp(self):
        print("this is precondition")

    def tearDown(self):
        print("this is post condition")

    @unittest.skip("skip this")
    def testfirst01(self):
        print("this is first case")

    def testfirst02(self):
        print("this is second test")


if __name__ =='__main__':
    #unittest.main()
    suite = unittest.TestSuite
    suite.addTest(FirstCase01('testfirst02'))
    unittest.TextTestRunner.run(suite)






