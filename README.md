# POO Fighting Game

Jogo de batalhas por turnos com artes ASCII e janela Pygame.
A torre tem nove adversários e um chefe.

## Executar e testar

Requer Python 3.12.

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python src/main.py
.venv\Scripts\python -m pytest
```

## Controles

| Tecla | Ação |
| --- | --- |
| 1, 2, 3 | Escolher ataque |
| P | Usar poção |
| Enter | Subir após vencer |
| R | Reiniciar com a classe atual |
| F1, F2, F3 | Começar outra torre como Guerreiro, Mago ou Arqueiro |
| Esc | Sair |

## Regras

- Guerreiro: 140 de vida. Mago: 110 de vida e 60 de mana. Arqueiro: 120 de vida.
- Cada classe tem três ataques. Dano, precisão e custo aparecem na tela.
- Um sorteio de 1 a 100 acerta quando o resultado é menor ou igual à precisão.
- Errar gasta o turno e o custo de mana. O cajado não gasta mana.
- O inimigo responde após um ataque ou uma poção, se ainda estiver vivo.
- Uma ação inválida não gasta turno, mana ou poção.
- O jogador começa com três poções. Cada uma cura até 50, respeitando a vida máxima.
- Entre lutas, o descanso recupera até 40 de vida e 40 de mana.
- As vitórias nas lutas 3, 6 e 9 dão uma poção. É possível usar poções no intervalo.
- A vida e a mana restantes continuam na próxima luta.
- O chefe tem 180 de vida. Com 90 ou menos, troca seu golpe pela fúria.
- Perder toda a vida encerra a partida. Derrotar o chefe vence a torre.

## Arquivos

| Arquivo | Responsabilidade |
| --- | --- |
| `src/main.py` | Iniciar o jogo |
| `src/personagens.py` | Personagens, ataques, mana e poções |
| `src/batalha.py` | Turnos, resultados e sequência de lutas |
| `src/interface.py` | Janela, teclado, textos e artes ASCII em `ARTES` |
| `tests/test_personagens.py` | Testar dano, ataques, recursos e subclasses |
| `tests/test_batalha.py` | Testar turnos e progressão da torre |
| `tests/__init__.py` | Permitir aos testes importar os arquivos de `src` |
| `requirements.txt` | Dependências do jogo e dos testes |
| `.gitignore` | Excluir ambiente virtual e arquivos gerados do Git |

## POO

`Personagem` concentra as regras de vida e ataque. As propriedades `vida` e `mana`
permitem consultar os valores; os métodos controlam suas alterações.
Guerreiro, Mago e Arqueiro herdam essa base. Orc e Chefe herdam de Inimigo.
Chefe sobrescreve `atacar()` para mudar o golpe quando entra em fúria.
`Batalha` usa a mesma operação de ataque para personagens diferentes.

Cada personagem possui seus ataques e inventário. `Torre` cria as lutas e
`Jogo` apresenta os resultados. As regras não dependem de Pygame.
Os testes usam `unittest` e `Mock`, executados por pytest.
O parâmetro `sortear` permite testar acertos e erros sem depender da sorte.

## Desenvolvimento

As atividades seguem uma issue, uma branch e um PR por funcionalidade.
Os testes são executados antes de cada merge. Trabalho individual, sem aprovação
de terceiro. A interface segue a estrutura do exemplo `outro_jogo.py` da aula.
