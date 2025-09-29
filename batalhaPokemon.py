from random import choice, random
import Pokemon as Pokemon

class Batalha:
    CHANCE_ACERTO = 0.85  # Chance de acerto de 85%

    def __init__(self, pokemon_jogador, pokemon_oponente):
        """
                O construtor da classe Batalha. Inicia a batalha com os dois pokémons.
                :param pokemon_jogador: Uma instância da classe Pokemon representando o jogador.
                :param pokemon_oponente: Uma instância da classe Pokemon representando o oponente.
         """
        self.pokemon_jogador = pokemon_jogador
        self.pokemon_oponente = pokemon_oponente

    def executar_ataque(self, atacante, defensor, ataque):
        # Verifica se o ataque acertou baseado na chance
        if random() <= self.CHANCE_ACERTO:
            dano = ataque['dano']
            defensor.receber_dano(dano)
            log_ataque = f"{atacante.nome} usou {ataque['nome']} e causou {dano} de dano em {defensor.nome}."
            log_hp = f"HP de {defensor.nome} agora é {defensor.hp}."

            return f"{log_ataque}\n{log_hp}"
        else:
            # O ataque errou
            return f"{atacante.nome} usou {ataque['nome']}, mas o ataque errou!"

    def ataque_do_oponente(self):
        ataque_escolhido = choice(self.pokemon_oponente.ataques)
        return self.executar_ataque(self.pokemon_oponente, self.pokemon_jogador, ataque_escolhido)

    def obter_vencedor(self):
        """
        Verifica o estado da batalha e retorna o vencedor se houver um.
        Usa o método 'esta_vivo()' dos próprios pokémons para verificar o HP.

        :return: A instância do Pokémon vencedor, ou None se a batalha ainda não terminou.
        """
        if not self.pokemon_jogador.esta_vivo():
            return self.pokemon_oponente
        elif not self.pokemon_oponente.esta_vivo():
            return self.pokemon_jogador
        return None