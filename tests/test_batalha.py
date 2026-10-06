import unittest
from unittest.mock import Mock
from personagens import Guerreiro, Inimigo
from batalha import Batalha


class TestBatalha(unittest.TestCase):
    def test_resposta_do_inimigo(self):
        p, alvo = Guerreiro(), Inimigo("Goblin", 65, 10, 80)
        Batalha(p, alvo, Mock(return_value=1)).agir()
        self.assertEqual((p.vida, alvo.vida), (130, 47))

    def test_derrotado_nao_responde(self):
        p, alvo = Guerreiro(), Inimigo("Alvo", 1, 50, 100)
        batalha = Batalha(p, alvo, Mock(return_value=1))
        batalha.agir()
        self.assertEqual(p.vida, 140)
        with self.assertRaises(ValueError):
            batalha.agir()
