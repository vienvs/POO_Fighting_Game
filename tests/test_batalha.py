import unittest
from unittest.mock import Mock
from personagens import Guerreiro, Inimigo
from batalha import Batalha, Torre


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

    def test_subir_torre_e_vencer(self):
        torre = Torre()
        torre.avancar()
        self.assertEqual(torre.andar, 1)
        for i in range(len(torre.inimigos)):
            torre.batalha.inimigo.receber_dano(999)
            torre.verificar_resultado()
            if i < len(torre.inimigos) - 1:
                self.assertEqual(torre.estado, "intervalo")
                torre.avancar()
        self.assertEqual(torre.estado, "vitoria")

    def test_derrota_impede_avanco(self):
        torre = Torre()
        torre.jogador.receber_dano(999)
        torre.verificar_resultado()
        torre.avancar()
        self.assertEqual((torre.estado, torre.andar), ("derrota", 1))

    def test_orc_na_torre(self):
        self.assertEqual(Torre().inimigos[1].nome, "Orc")

    def test_nove_inimigos_e_um_chefe(self):
        torre = Torre()
        self.assertEqual(len(torre.inimigos), 10)
        self.assertEqual(torre.inimigos[-1].nome, "Guardiao da torre")
