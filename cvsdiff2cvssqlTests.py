
import unittest
from csvdiff2csvsql import diff2sql

class MyTestCase(unittest.TestCase):
    def test_default_greeting_set(self):
        diff = '''
{
  "_index": [
    "zero", 
    "one"
  ], 
  "added": [
    {
      "one": "r", 
      "three": "t", 
      "two": "s", 
      "zero": "p"
    }
  ], 
  "changed": [
    {
      "fields": {
        "two": {
          "from": "g", 
          "to": "xxx"
        }
      }, 
      "key": [
        "e", 
        "f"
      ]
    }, 
    {
      "fields": {
        "three": {
          "from": "p", 
          "to": "xxx"
        }, 
        "two": {
          "from": "o", 
          "to": "p"
        }
      }, 
      "key": [
        "m", 
        "n"
      ]
    }
  ], 
  "removed": [
    {
      "one": "b", 
      "three": "d", 
      "two": "c", 
      "zero": "a"
    }
  ]
}
'''
        expected = '''
csvsql --query "select * from left where zero='e' and one='f'" left.csv
csvsql --query "select * from right where zero='m' and one='n'" right.csv
csvsql --query "select * from left where zero='e' and one='f'" left.csv
csvsql --query "select * from right where zero='m' and one='n'" right.csv
'''
        result = diff2sql(diff)
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()