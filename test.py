import unittest
import requests

class TestStringMethods(unittest.TestCase):

    def test_add_user(self):
        req = requests.post("http://127.0.0.1:5000/api", data={
            "action": "add-user",
            "data": "ScreenMix"
        })
        self.assertEqual(req.json()["status"], 200)

    def test_add_user2(self):
        req = requests.post("http://127.0.0.1:5000/api", data={
            "action": "add-user",
            "data": "https://twitter.com/s_3039"
        })
        self.assertEqual(req.json()["status"], 200)

    def test_list_users(self):
        req = requests.post("http://127.0.0.1:5000/api", data={
            "action": "list-users",
        })
        print(req.json()["users"])
        self.assertEqual(req.json()["status"], 200)

    def test_set_time(self):
        req = requests.post("http://127.0.0.1:5000/api", data={
            "action": "set-time",
            "data": 10
        })
        self.assertEqual(req.json()["status"], 200)

if __name__ == '__main__':
    unittest.main()