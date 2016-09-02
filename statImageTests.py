import unittest
from viewer import statisticImage

class statImageTestCase(unittest.TestCase):

	def test_tStat(self):
	
		self.assertEqual("T", statisticImage("http://purl.obolibrary.org/obo/STATO_0000176"))
		

	def test_fStat(self):
	
		self.assertEqual("F", statisticImage("http://purl.obolibrary.org/obo/STATO_0000282"))
		
	def test_zStat(self):
	
		self.assertEqual("Z", statisticImage("http://purl.obolibrary.org/obo/STATO_0000376"))

unittest.main()