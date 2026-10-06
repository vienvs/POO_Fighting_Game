import unittest
from unittest.mock import Mock
from personagens import Personagem, Ataque, Guerreiro, Inimigo, Mago, PocaoVida


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

    def test_ataques_guerreiro(self):
        p, alvo = Guerreiro(), Personagem("Alvo", 100)
        self.assertEqual(len(p.ataques), 3)
        p.atacar(alvo, 1, Mock(return_value=80))
        self.assertEqual(alvo.vida, 70)
        p.atacar(alvo, 1, Mock(return_value=81))
        self.assertEqual(alvo.vida, 70)

    def test_ataque_inimigo(self):
        p = Guerreiro()
        Inimigo("Goblin", 65, 10, 80).atacar(p, sortear=Mock(return_value=1))
        self.assertEqual(p.vida, 130)

    def test_cajado_mago(self):
        p, alvo = Mago(), Guerreiro()
        p.atacar(alvo, sortear=Mock(return_value=1))
        self.assertEqual(alvo.vida, 124)

    def test_magia_mago(self):
        p, alvo = Mago(), Guerreiro()
        p.atacar(alvo, 1, Mock(return_value=1))
        self.assertEqual((alvo.vida, p.mana), (106, 52))
        p.atacar(alvo, 2, Mock(return_value=100))
        self.assertEqual(p.mana, 38)

    def test_pocao_cura_com_limite(self):
        p = Guerreiro()
        p.receber_dano(20)
        PocaoVida().usar(p)
        self.assertEqual(p.vida, 140)
        with self.assertRaises(ValueError):
            PocaoVida().usar(p)
