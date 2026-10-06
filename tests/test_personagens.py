import unittest
from unittest.mock import Mock
from personagens import Personagem


class TestPersonagens(unittest.TestCase):
    def test_personagem_comeca_vivo(self):
        p = Personagem("Teste", 100)
        self.assertEqual(p.vida, 100)
        self.assertTrue(p.esta_vivo())

    def test_receber_dano(self):
        p = Personagem("Teste", 100)
        self.assertEqual(p.receber_dano(30), 30)
        self.assertEqual(p.vida, 70)
        with self.assertRaises(ValueError):
            p.receber_dano(-1)
        self.assertEqual(p.receber_dano(200), 70)
        self.assertFalse(p.esta_vivo())
