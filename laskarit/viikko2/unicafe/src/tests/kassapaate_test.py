import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
        self.maksukortti = Maksukortti(500)
        self.koyhakortti = Maksukortti(200)

    def test_kassapaate(self):
        self.assertEqual(str(self.kassapaate.kassassa_rahaa), "100000")
        self.assertEqual(str(self.kassapaate.edulliset), "0")
        self.assertEqual(str(self.kassapaate.maukkaat), "0")

    def test_käteisosto_edullisesti(self):
        self.kassapaate.syo_edullisesti_kateisella(240)
        self.assertEqual(str(self.kassapaate.kassassa_rahaa), "100240")
        self.assertEqual(str(self.kassapaate.syo_edullisesti_kateisella(450)), "210")
    
    def test_käteisosto_maukkaasti(self):
        self.kassapaate.syo_maukkaasti_kateisella(450) 
        self.assertEqual(str(self.kassapaate.kassassa_rahaa), "100400")
        self.assertEqual(str(self.kassapaate.syo_maukkaasti_kateisella(450)), "50")

    def test_myydy_maukkaat(self):
        self.kassapaate.syo_maukkaasti_kateisella(450)
        self.assertEqual(str(self.kassapaate.maukkaat), "1") 
    def test_myydy_edulliset(self):  
        self.kassapaate.syo_edullisesti_kateisella(240)
        self.assertEqual(str(self.kassapaate.edulliset), "1")
    def test_myydy_lounaat_ei_rahaa(self):
        self.kassapaate.syo_maukkaasti_kateisella(300)
        self.kassapaate.syo_edullisesti_kateisella(200)
        self.assertEqual(str(self.kassapaate.maukkaat), "0")
        self.assertEqual(str(self.kassapaate.edulliset), "0")
    
    def test_käteisosto_ei_rahaa(self): 
        self.kassapaate.syo_maukkaasti_kateisella(300)
        self.kassapaate.syo_edullisesti_kateisella(200)
        self.assertEqual(str(self.kassapaate.kassassa_rahaa), "100000")
        self.assertEqual(str(self.kassapaate.syo_maukkaasti_kateisella(300)), "300")
        self.assertEqual(str(self.kassapaate.syo_edullisesti_kateisella(200)), "200")

    def test_syo_edullisesti_kortilla(self):
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(str(self.maksukortti), "saldo: 2.6")
        self.assertEqual(str(self.kassapaate.edulliset), "1")

    def test_syo_maukkaasti_kortilla(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertEqual(str(self.maksukortti), "saldo: 1.0")
        self.assertEqual(str(self.kassapaate.maukkaat), "1")

    def test_on_rahaa_kortilla(self):
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(str(self.maksukortti), "saldo: 2.6")
        self.assertEqual(str(self.kassapaate.edulliset), "1")

    def test_ei_rahaa_kortilla(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.koyhakortti)
        self.assertEqual(str(self.koyhakortti), "saldo: 2.0")
        self.assertEqual(str(self.kassapaate.maukkaat), "0")

        self.kassapaate.syo_edullisesti_kortilla(self.koyhakortti)
        self.assertEqual(str(self.koyhakortti), "saldo: 2.0")
        self.assertEqual(str(self.kassapaate.edulliset), "0")

    def test_true_false(self):
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(self.maksukortti), True)
        self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti), False)
    
    def test_kassa_ei_muutu(self):
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(str(self.kassapaate.kassassa_rahaa), "100000")

    def test_lataa_rahaa_kortille(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, 100)
        self.assertEqual(str(self.kassapaate.kassassa_rahaa), "100100")
        self.assertEqual(str(self.maksukortti), "saldo: 6.0")