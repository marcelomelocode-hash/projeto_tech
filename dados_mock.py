from __future__ import annotations


# Estrutura temporária (mock) para votos
VOTOS_MOCK: dict[str, dict[str, int]] = {
    "jornada": {
        "Entusiasta / Curioso": 28,
        "Estudante / Iniciante": 46,
        "Profissional Júnior": 34,
        "Profissional Pleno / Sênior": 22,
        "Liderança / Gestão": 16,
    },
    "interesses": {
        "Como desenvolver sua própria IA": 52,
        "C++": 18,
        "Curso de C#": 25,
        "Desenvolvimento Web": 41,
        "Java": 30,
        "Lógica de Programação": 38,
        "Machine Learning": 47,
        "Python": 55,
        "SQL": 21,
        "Segurança da Informação": 33,
        "UI/UX Design": 27,
    },
}


def calcular_percentuais(votos: dict[str, int]) -> list[tuple[str, int, float]]:
    """
    Retorna lista no formato:
    [(nome_opcao, votos, percentual), ...]

    percentual = (votos_opcao / total_votos) * 100
    """
    total_votos = sum(votos.values())
    if total_votos <= 0:
        return [(opcao, qtd, 0.0) for opcao, qtd in votos.items()]

    return [
        (opcao, qtd, (qtd / total_votos) * 100)
        for opcao, qtd in votos.items()
    ]


def top_n_interesses(n: int = 5) -> list[tuple[str, int, float]]:
    base = calcular_percentuais(VOTOS_MOCK["interesses"])
    return sorted(base, key=lambda item: item[1], reverse=True)[:n]


def ranking_jornada() -> list[tuple[str, int, float]]:
    base = calcular_percentuais(VOTOS_MOCK["jornada"])
    return sorted(base, key=lambda item: item[1], reverse=True)

