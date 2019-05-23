
import unittest
import json
from csvdiff2csvsql import modified_to_queries
from csvdiff2csvsql import added_to_queries
from csvdiff2csvsql import removed_to_queries


class Cvsdiff2CvssqlTests(unittest.TestCase):

    def test_modified_to_queries(self):
        diff = '''
    {
      "_index": [
        "zero", 
        "one"
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
      ] 
    }
    '''
        expected = '''csvsql --query "select * from left where 1=1 and zero='e' and one='f'" left.csv
csvsql --query "select * from right where 1=1 and zero='e' and one='f'" right.csv
csvsql --query "select * from left where 1=1 and zero='m' and one='n'" left.csv
csvsql --query "select * from right where 1=1 and zero='m' and one='n'" right.csv'''
        result = modified_to_queries(json.loads(diff), "left", "right")
        self.assertEqual(result.strip(), expected.strip())


    def test_added_to_queries(self):
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
        },
        {
          "one": "u", 
          "three": "v", 
          "two": "w", 
          "zero": "x"
        }
      ]
    }
    '''
        expected = '''csvsql --query "select * from right where 1=1 and zero='p' and one='r'" right.csv
csvsql --query "select * from right where 1=1 and zero='x' and one='u'" right.csv'''
        result = added_to_queries(json.loads(diff), "right")
        self.assertEqual(result.strip(), expected.strip())


    def test_removed_to_queries(self):
        diff = '''
    {
      "_index": [
        "zero", 
        "one"
      ], 
      "removed": [
        {
          "one": "r", 
          "three": "t", 
          "two": "s", 
          "zero": "p"
        },
        {
          "one": "u", 
          "three": "v", 
          "two": "w", 
          "zero": "x"
        }
      ]
    }
    '''
        expected = '''csvsql --query "select * from left where 1=1 and zero='p' and one='r'" left.csv
csvsql --query "select * from left where 1=1 and zero='x' and one='u'" left.csv'''
        result = removed_to_queries(json.loads(diff), "left")
        self.assertEqual(result.strip(), expected.strip())


if __name__ == '__main__':
    unittest.main()