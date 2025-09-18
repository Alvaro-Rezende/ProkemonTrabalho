class Pokemon: # Classe para representar um Pokémon(Init é o construtor da classe).
    def __init__(self, nome, tipo, hp, ataques, descricao, imagem): # Self é a referência ao próprio objeto.
        self.nome = nome
        self.tipo = tipo
        self.hp = hp
        self.ataques = ataques 
        self.descricao = descricao
        self.imagem = imagem     
        
    def atacar(self, outro_pokemon, ataque_escolhido):
        nome_ataque = ataque_escolhido["nome"]
        dano_ataque = ataque_escolhido["dano"]
        
        print(f"{self.nome} usou {nome_ataque} em {outro_pokemon.nome}!")
        outro_pokemon.hp -= dano_ataque
        print(f"{outro_pokemon.nome} agora tem {outro_pokemon.hp} de HP.")    
     
    def esta_vivo(self):
        return self.hp > 0    
    
    
# DADOS DOS POKÉMONS
POKEDEX_DATA = [
    {"nome": "Eevee", "tipo": "Normal", "hp": 90, "ataques":[
            {"nome": "Bite", "dano": 30},
            {"nome": "Tail Whip", "dano": 15}
        ],
        "descrição": "Eevee tem uma estrutura genética instável que pode evoluir para muitos tipos diferentes de Pokémon dependendo de seu ambiente.",
        "imagem": "eevee.png"
    },
    {"nome": "Gengar", "tipo": "Fantasma", "hp": 100, "ataques": [
            {"nome": "Shadow Ball", "dano": 25},
            {"nome": "Dark Pulse", "dano": 30}
        ],
        "descrição": "Gengar é conhecido por sua natureza travessa e por pregar peças em pessoas e Pokémon. Dizem que ele se esconde nas sombras, esperando o momento certo para atacar.",
        "imagem": "gengar.png"
     },
    {"nome": "Lucario", "tipo": "Metal", "hp": 110, "ataques": [
            {"nome": "Thunder Punch", "dano": 30},
            {"nome": "Steel Beam", "dano": 35}
        ],
        "descrição": "Dizem que nenhum inimigo pode permanecer invisível para Lucario, já que ele pode detectar auras — até mesmo aquelas de inimigos que ele não conseguiria ver de outra forma.",
        "imagem": "lucario.png"
     },
    {"nome": "Charizard", "tipo": "Fogo", "hp": 105, "ataques": [
            {"nome": "Dragon Claw", "dano": 25},
            {"nome": "Flare Blitz", "dano": 35}
        ],
        "descrição": "Se Charizard ficar realmente irritado, a chama na ponta de sua cauda queima em um tom azul claro.",
        "imagem": "charizard.png"
    },
    {"nome": "Bulbasaur", "tipo": "Planta", "hp": 95, "ataques": [
            {"nome": "Vine Whip", "dano": 20},
            {"nome": "Razor Leaf", "dano": 25}
        ],
        "descrição": "Por algum tempo após o nascimento, ele usa os nutrientes contidos na semente em suas costas para crescer.",
        "imagem": "bulbasaur.png"
    },
    {"nome": "Picachu", "tipo": "Elétrico", "hp": 90, "ataques": [
            {"nome": "Thunder Shock", "dano": 20}, 
            {"nome": "Electro Ball", "dano": 30}
        ],
        "descrição": "Quando fica irritado, ele imediatamente descarrega a energia armazenada nas bolsas em suas bochechas.",
        "imagem": "pikachu.png"
    }
]

# FUNÇÃO PARA CRIAR/BUSCAR UM POKÉMON
def criar_pokemon(nome):
    """Busca um Pokémon na POKEDEX_DATA pelo nome e retorna um objeto Pokemon."""
    for dados in POKEDEX_DATA:
        if dados["nome"].lower() == nome.lower():
            return Pokemon(dados["nome"], dados["tipo"], dados["hp"], dados["ataques"], dados["descrição"], dados["imagem"])
    return None