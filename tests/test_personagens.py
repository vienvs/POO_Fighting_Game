import unittest
from unittest.mock import Mock
from personagens import Personagem, Guerreiro, Mago, Arqueiro, Ataque, PocaoVida, Inimigo, Orc, Chefe


class TestPersonagens(unittest.TestCase):
    def test_dano_limitado_e_zero(self):
        p = Guerreiro()
        self.assertEqual(p.receber_dano(0), 0)
        self.assertEqual(p.receber_dano(30), 30)
        self.assertEqual(p.vida, 110)
        self.assertEqual(p.receber_dano(999), 110)
        self.assertFalse(p.esta_vivo())

    def test_dano_invalido_preserva_vida(self):
        p = Guerreiro()
        for dano in (-1, 1.5, True, "10"):
            with self.assertRaises(ValueError):
                p.receber_dano(dano)
        self.assertEqual(p.vida, 140)
        with self.assertRaises(AttributeError):
            p.vida = -10

    def test_construtores_validam_dados(self):
        with self.assertRaises(ValueError):
            Personagem("Teste", 0)
        with self.assertRaises(ValueError):
            Personagem("Teste", 100, -1)
        for precisao in (-1, 101, True):
            with self.assertRaises(ValueError):
                Ataque("Teste", 10, precisao)

    def test_tres_classes_tres_ataques(self):
        for classe in (Guerreiro, Mago, Arqueiro):
            p, alvo = classe(), Guerreiro()
            self.assertEqual(len(p.ataques), 3)
            p.atacar(alvo, sortear=Mock(return_value=1))
            self.assertEqual(alvo.vida, alvo.vida_maxima - p.ataques[0].dano)

    def test_extremos_e_limite_da_precisao(self):
        p, alvo = Guerreiro(), Guerreiro()
        p.ataques = [Ataque("Nunca", 10, 0), Ataque("Sempre", 10, 100),
                     Ataque("Limite", 10, 80)]
        p.atacar(alvo, 0, Mock(return_value=1))
        self.assertEqual(alvo.vida, 140)
        p.atacar(alvo, 1, Mock(return_value=100))
        p.atacar(alvo, 2, Mock(return_value=80))
        p.atacar(alvo, 2, Mock(return_value=81))
        self.assertEqual(alvo.vida, 120)

    def test_magia_gasta_mana_mesmo_errando(self):
        p, alvo = Mago(), Guerreiro()
        p.atacar(alvo, 1, Mock(return_value=100))
        self.assertEqual(p.mana, 52)
        self.assertEqual(alvo.vida, 140)
        with self.assertRaises(AttributeError):
            p.mana = 100

    def test_sem_mana_nao_sorteia_nem_muda_alvo(self):
        p, alvo = Mago(), Personagem("Alvo", 1000)
        for _ in range(7):
            p.atacar(alvo, 1, Mock(return_value=100))
        sorteio = Mock()
        with self.assertRaises(ValueError):
            p.atacar(alvo, 1, sorteio)
        sorteio.assert_not_called()
        self.assertEqual(p.mana, 4)
        self.assertEqual(alvo.vida, 1000)
        p.atacar(alvo, 0, Mock(return_value=1))
        self.assertEqual(p.mana, 4)

    def test_pocao_so_consumida_apos_cura(self):
        p = Guerreiro()
        p.inventario = [PocaoVida()]
        with self.assertRaises(ValueError):
            p.usar_pocao()
        self.assertEqual(len(p.inventario), 1)
        p.receber_dano(20)
        p.usar_pocao()
        self.assertEqual(p.vida, 140)
        self.assertEqual(p.inventario, [])
        with self.assertRaises(ValueError):
            p.usar_pocao()

    def test_morto_nao_cura_descansa_ou_ataca(self):
        p, alvo = Guerreiro(), Guerreiro()
        p.receber_dano(999)
        with self.assertRaises(ValueError):
            p.curar(50)
        with self.assertRaises(ValueError):
            p.descansar()
        with self.assertRaises(ValueError):
            p.atacar(alvo)
        self.assertEqual(p.vida, 0)

    def test_descanso_recupera_e_respeita_limites(self):
        p, alvo = Mago(), Guerreiro()
        p.receber_dano(80)
        for _ in range(3):
            p.atacar(alvo, 2, Mock(return_value=100))
        p.descansar()
        self.assertEqual((p.vida, p.mana), (70, 58))
        p.descansar()
        self.assertEqual((p.vida, p.mana), (110, 60))

    def test_inventarios_independentes(self):
        a, b = Guerreiro(), Guerreiro()
        a.inventario.append(PocaoVida())
        self.assertEqual(b.inventario, [])


    def test_ataque_inimigo(self):
        p = Guerreiro()
        Inimigo("Goblin", 65, 10, 80).atacar(p, sortear=Mock(return_value=1))
        self.assertEqual(p.vida, 130)

    def test_orc(self):
        p, orc = Guerreiro(), Orc()
        self.assertIsInstance(orc, Inimigo)
        orc.atacar(p, sortear=Mock(return_value=1))
        self.assertEqual(p.vida, 126)

    def test_furia_chefe(self):
        p, chefe = Guerreiro(), Chefe()
        chefe.atacar(p, sortear=Mock(return_value=1))
        self.assertEqual(p.vida, 116)
        chefe.receber_dano(90)
        chefe.atacar(p, sortear=Mock(return_value=1))
        self.assertEqual(p.vida, 84)
