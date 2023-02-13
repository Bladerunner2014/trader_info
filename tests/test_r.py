import unittest
import requests


class TestAPI(unittest.TestCase):
    # for Postgres tsets
    URL = " http://127.0.0.1:5001/v1/trader/reza"
    URL1 = " http://127.0.0.1:5001/v1/trader"
    data = {"user_id": "mohammad134", "summary_file": "parham", "bio": "ali"}

    data1 = {"user_id": "mohammad134", "summary_file": "par", "bio": "ai"}

    # for MINIO tests
    URL3 = " http://127.0.0.1:5001/v1/trader/upload"
    URL4 = " http://127.0.0.1:5001/v1/trader/download"
    header = {"user_id": "jayson1jdcj"}

    def test_1(self):
        resp = requests.get(self.URL)
        self.assertEqual(resp.status_code, 200)
        print('test 1 completed')

    def test_2(self):
        resp = requests.post(self.URL1, json=self.data)
        self.assertEqual(resp.status_code, 200)
        print('test 2 completed')

    def test_3(self):
        resp = requests.put(self.URL1, json=self.data1)
        self.assertEqual(resp.status_code, 200)
        print('test 3 completed')

    def test_4(self):
        resp = requests.post(self.URL1, data="salm", headers=self.header)
        self.assertEqual(resp.status_code, 200)
        print('test 4 completed')

    def test_5(self):
        resp = requests.post(self.URL1,headers=self.header)
        self.assertEqual(resp.status_code, 200)
        print('test 5 completed')


if __name__ == "__main__":
    tester = TestAPI()

    tester.test_1()
    tester.test_2()
    tester.test_3()
    tester.test_4()
    tester.test_5()
