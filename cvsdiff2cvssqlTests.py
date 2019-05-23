
import unittest
from csvdiff2csvsql import modified_to_queries

class Cvsdiff2CvssqlTests(unittest.TestCase):
    def test_modified_to_queries(self):
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
        expected = '''csvsql --query "select * from left where 1=1 and zero='e' and one='f'" left.csv
csvsql --query "select * from right where 1=1 and zero='e' and one='f'" right.csv
csvsql --query "select * from left where 1=1 and zero='m' and one='n'" left.csv
csvsql --query "select * from right where 1=1 and zero='m' and one='n'" right.csv'''
        result = modified_to_queries(diff, "left", "right")
        self.assertEqual(result.strip(), expected.strip())

if __name__ == '__main__':
    unittest.main()