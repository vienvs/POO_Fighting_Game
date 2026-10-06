import unittest
from unittest.mock import Mock
from personagens import Personagem


class TestPersonagens(unittest.TestCase):
    def test_personagem_comeca_vivo(self):
        p = Personagem("Teste", 100)
        self.assertEqual(p.vida, 100)
        self.assertTrue(p.esta_vivo())
