import unittest
from unittest.mock import Mock
from batalha import Batalha, Torre
from personagens import Guerreiro, Mago, Arqueiro, Inimigo, Orc, Chefe, PocaoVida


class TestBatalha(unittest.TestCase):
    def test_erro_de_ataque_gasta_turno(self):
        p, alvo = Guerreiro(), Inimigo("Orc", 100, 15, 80)
        Batalha(p, alvo, Mock(side_effect=[100, 1])).agir()
        self.assertEqual((p.vida, alvo.vida), (125, 100))

    def test_acao_invalida_nao_passa_turno(self):
        p, alvo, sorteio = Guerreiro(), Chefe(), Mock()
        batalha = Batalha(p, alvo, sorteio)
        for indice in (-1, 3, True):
            with self.assertRaises(ValueError):
                batalha.agir(indice)
        with self.assertRaises(ValueError):
            batalha.agir(pocao=True)
        sorteio.assert_not_called()

    def test_mana_insuficiente_nao_passa_turno(self):
        p, alvo = Mago(), Chefe()
        for _ in range(4):
            p.atacar(alvo, 2, Mock(return_value=100))
        sorteio = Mock()
        with self.assertRaises(ValueError):
            Batalha(p, alvo, sorteio).agir(1)
        sorteio.assert_not_called()
        self.assertEqual(p.vida, 110)

    def test_pocao_em_batalha_permite_resposta(self):
        p, alvo = Guerreiro(), Inimigo("Orc", 100, 15, 80)
        p.inventario = [PocaoVida()]
        p.receber_dano(80)
        Batalha(p, alvo, Mock(return_value=1)).agir(pocao=True)
        self.assertEqual(p.vida, 95)
        self.assertEqual(p.inventario, [])

    def test_derrotado_nao_contra_ataca(self):
        p, alvo = Guerreiro(), Inimigo("Alvo", 1, 50, 100)
        sorteio = Mock(return_value=1)
        batalha = Batalha(p, alvo, sorteio)
        self.assertEqual(len(batalha.agir()), 1)
        self.assertEqual(p.vida, 140)
        self.assertTrue(batalha.finalizada)
        sorteio.assert_called_once()
        with self.assertRaises(ValueError):
            batalha.agir()
        with self.assertRaises(ValueError):
            Batalha(p, alvo)

    def test_chefe_entra_em_furia_na_metade_da_vida(self):
        chefe, p = Chefe(), Guerreiro()
        chefe.atacar(p, sortear=Mock(return_value=1))
        self.assertEqual(p.vida, 116)
        chefe.receber_dano(90)
        chefe.atacar(p, sortear=Mock(return_value=1))
        self.assertEqual(p.vida, 84)


class TestTorre(unittest.TestCase):
    def vencer(self, torre):
        torre.batalha.inimigo.receber_dano(999)
        torre.verificar_resultado()

    def test_exatamente_nove_normais_e_um_chefe(self):
        torre = Torre()
        self.assertEqual(len(torre.inimigos), 10)
        for inimigo in torre.inimigos[:9]:
            self.assertIsInstance(inimigo, Inimigo)
            self.assertNotIsInstance(inimigo, Chefe)
        self.assertIsInstance(torre.inimigos[1], Orc)
        self.assertIsInstance(torre.inimigos[-1], Chefe)

    def test_avanca_apenas_apos_vitoria_e_recompensa_uma_vez(self):
        torre = Torre()
        torre.avancar()
        self.assertEqual(torre.andar, 1)
        for andar in range(1, 10):
            self.assertEqual(torre.andar, andar)
            self.vencer(torre)
            self.assertEqual(torre.estado, "intervalo")
            self.assertEqual(len(torre.jogador.inventario), 3 + andar // 3)
            torre.verificar_resultado()
            torre.agir(0)
            self.assertEqual(len(torre.jogador.inventario), 3 + andar // 3)
            torre.avancar()
        self.assertEqual(torre.andar, 10)
        self.vencer(torre)
        self.assertEqual(torre.estado, "vitoria")
        torre.avancar()
        torre.agir()
        self.assertEqual(torre.andar, 10)

    def test_intervalo_conserva_dano_restante_e_pocao_nao_contra_ataca(self):
        torre = Torre()
        torre.jogador.receber_dano(100)
        self.vencer(torre)
        self.assertEqual(torre.jogador.vida, 80)
        torre.agir(pocao=True)
        self.assertEqual(torre.jogador.vida, 130)
        torre.avancar()
        self.assertEqual(torre.jogador.vida, 130)

    def test_derrota_bloqueia_acoes_e_avanco(self):
        torre = Torre()
        torre.jogador.receber_dano(999)
        torre.verificar_resultado()
        torre.agir(pocao=True)
        torre.avancar()
        self.assertEqual((torre.estado, torre.andar, torre.jogador.vida), ("derrota", 1, 0))

    def test_tres_classes_podem_vencer_com_sorteio_controlado(self):
        for classe in (Guerreiro, Mago, Arqueiro):
            torre = Torre(classe, Mock(return_value=1))
            for _ in range(500):
                p = torre.jogador
                if torre.estado in ("vitoria", "derrota"):
                    break
                if torre.estado == "intervalo":
                    if p.vida_maxima - p.vida >= 50 and p.inventario:
                        torre.agir(pocao=True)
                    else:
                        torre.avancar()
                elif p.vida <= 45 and p.inventario:
                    torre.agir(pocao=True)
                else:
                    indice = 0
                    for i, ataque in enumerate(p.ataques):
                        if ataque.mana <= p.mana:
                            if ataque.dano > p.ataques[indice].dano:
                                indice = i
                    torre.agir(indice)
            self.assertEqual(torre.estado, "vitoria", classe.__name__)
