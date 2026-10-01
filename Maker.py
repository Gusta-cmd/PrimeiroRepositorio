from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    Boolean,
    insert,
    select,
    update
)

# ==========================================
# 1. CONEXÃO COM O BANCO DE DADOS
# ==========================================

engine = create_engine(
    "mysql+pymysql://root:ifmt2026@localhost/biblioteca"
)

metadata = MetaData()


# ==========================================
# 2. MODELAGEM DA TABELA
# ==========================================

livros = Table(
    "livros",
    metadata,

    Column(
        "id",
        Integer,
        primary_key=True,
        autoincrement=True
    ),

    Column(
        "titulo",
        String(150),
        nullable=False
    ),

    Column(
        "autor",
        String(100),
        nullable=False
    ),

    Column(
        "ano",
        Integer
    ),

    Column(
        "disponivel",
        Boolean,
        default=True,
        nullable=False
    )
)

# Criação da tabela
metadata.create_all(engine)

print("Banco de dados conectado!")
print("Tabela 'livros' criada/verificada com sucesso!")


# ==========================================
# 3. CADASTRO INICIAL
# ==========================================

livros_iniciais = [
    {
        "titulo": "Dom Casmurro",
        "autor": "Machado de Assis",
        "ano": 1899,
        "disponivel": True
    },

    {
        "titulo": "O Pequeno Príncipe",
        "autor": "Antoine de Saint-Exupéry",
        "ano": 1943,
        "disponivel": True
    },

    {
        "titulo": "1984",
        "autor": "George Orwell",
        "ano": 1949,
        "disponivel": True
    },

    {
        "titulo": "Harry Potter e a Pedra Filosofal",
        "autor": "J. K. Rowling",
        "ano": 1997,
        "disponivel": True
    }
]

with engine.connect() as conn:

    comando = insert(livros).values(livros_iniciais)

    conn.execute(comando)
    conn.commit()

print("\nLivros cadastrados com sucesso!")


# ==========================================
# 4. CONSULTA DOS LIVROS DISPONÍVEIS
# ==========================================

with engine.connect() as conn:

    comando = select(livros).where(
        livros.c.disponivel == True
    )

    resultado = conn.execute(comando)

    print("\n===== LIVROS DISPONÍVEIS =====")

    for livro in resultado:

        print(
            f"ID: {livro.id} | "
            f"Título: {livro.titulo} | "
            f"Autor: {livro.autor} | "
            f"Ano: {livro.ano}"
        )


# ==========================================
# 5. SIMULAÇÃO DE EMPRÉSTIMO
# ==========================================

id_livro = 1

with engine.connect() as conn:

    # Procura o livro
    consulta = select(livros).where(
        livros.c.id == id_livro
    )

    livro = conn.execute(consulta).fetchone()

    if livro is None:

        print("\nLivro não encontrado!")

    elif not livro.disponivel:

        print("\nO livro já está emprestado!")

    else:

        # Atualiza a disponibilidade
        comando = update(livros).where(
            livros.c.id == id_livro
        ).values(
            disponivel=False
        )

        conn.execute(comando)
        conn.commit()

        print(
            f"\nEmpréstimo realizado: "
            f"{livro.titulo}"
        )


# ==========================================
# 6. DEVOLUÇÃO DO LIVRO
# ==========================================

with engine.connect() as conn:

    comando = update(livros).where(
        livros.c.id == id_livro
    ).values(
        disponivel=True
    )

    conn.execute(comando)
    conn.commit()

print("\nLivro devolvido com sucesso!")


# ==========================================
# 7. VALIDAÇÃO FINAL
# ==========================================

with engine.connect() as conn:

    comando = select(livros)

    resultado = conn.execute(comando)

    print("\n===== SITUAÇÃO FINAL DO ACERVO =====")

    for livro in resultado:

        if livro.disponivel:
            status = "Disponível"
        else:
            status = "Emprestado"

        print(
            f"ID: {livro.id} | "
            f"{livro.titulo} | "
            f"Status: {status}"
        )

print("\nSistema finalizado!")
