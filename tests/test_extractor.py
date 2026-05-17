import unittest
from src.extractor import estrai_dati

class TestExtractor(unittest.TestCase):
    def test_estrai_dati_base(self):
        # TODO: Aggiungere test reali con file di cedolini d'esempio
        risultato = estrai_dati("dummy_path")
        self.assertIsInstance(risultato, dict)

if __name__ == '__main__':
    unittest.main()
