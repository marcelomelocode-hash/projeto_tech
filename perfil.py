import flet as ft
import asyncio
from cadastroTech import criar_radar
from conexao import conectar, fechar_conexao


def _obter_distribuicao_jornada() -> list[tuple[str, int, float]]:
    conexao = conectar()
    if not conexao:
        return []

    cursor = conexao.cursor()
    try:
        cursor.execute(
            "SELECT jornada FROM tbl_cadastro WHERE jornada IS NOT NULL AND jornada != ''"
        )
        linhas = cursor.fetchall()

        if not linhas:
            return []

        contagem: dict[str, int] = {}
        for (jornada,) in linhas:
            contagem[jornada] = contagem.get(jornada, 0) + 1

        total = sum(contagem.values())
        if total == 0:
            return []

        ordenados = sorted(contagem.items(), key=lambda x: x[1], reverse=True)
        return [(nome, qtd, (qtd / total) * 100) for nome, qtd in ordenados]

    except Exception as e:
        print(f"Erro ao consultar jornada: {e}")
        return []
    finally:
        cursor.close()
        fechar_conexao(conexao)


def show_perfil_screen(page: ft.Page, nome_usuario: str = "") -> None:
    page.clean()
    page.title = "Radar Tech - Perfil"
    page.bgcolor = ft.Colors.BLACK
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO

    radar, ponteiro = criar_radar()
    nome = (nome_usuario or "RADARTECH").upper()

    dados_jornada = _obter_distribuicao_jornada()

    barras: list[ft.Container] = []
    altura_barra = 40

    if not dados_jornada:
        barras.append(
            ft.Container(
                content=ft.Text("Nenhum dado de jornada disponível.", color=ft.Colors.WHITE54, size=12),
                padding=10,
            )
        )
    else:
        for idx, (jornada_nome, votos, percentual) in enumerate(dados_jornada):
            texto_barra = f"{jornada_nome}"
            tooltip_texto = f"{jornada_nome}: {votos} voto(s) ({percentual:.1f}%)"

            barras.append(
                ft.Container(
                    width=340,
                    height=altura_barra,
                    tooltip=tooltip_texto,
                    content=ft.Row(
                        controls=[
                            ft.Container(
                                width=28,
                                height=28,
                                border_radius=14,
                bgcolor=ft.Colors.CYAN_ACCENT_400 if idx == 0 else ft.Colors.with_opacity(0.5, ft.Colors.CYAN_ACCENT_400),
                alignment=ft.alignment.Alignment(0, 0),
                            ),
                            ft.Container(
                                width=200,
                                height=altura_barra - 6,
                                bgcolor=ft.Colors.CYAN_ACCENT_200 if idx == 0 else ft.Colors.with_opacity(0.5, ft.Colors.CYAN_ACCENT_400),
                                border_radius=10,
                                alignment=ft.alignment.Alignment(-1, 0),
                                padding=ft.padding.only(left=12),
                                content=ft.Text(
                                    texto_barra,
                                    size=13,
                                    color=ft.Colors.BLACK,
                                    weight=ft.FontWeight.BOLD,
                                ),
                            ),
                            ft.Container(
                                width=70,
                alignment=ft.alignment.Alignment(1, 0),
                                content=ft.Text(
                                    f"{percentual:.1f}%",
                                    size=14,
                                    color=ft.Colors.WHITE,
                                    weight=ft.FontWeight.BOLD,
                                ),
                            ),
                        ],
                        spacing=8,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                )
            )

    def abrir_tendencia(_: ft.ControlEvent) -> None:
        from tendencia import show_tendencia_screen
        show_tendencia_screen(page, nome)

    def abrir_estrategia(_: ft.ControlEvent) -> None:
        from estrategia import show_estrateguia_screen
        show_estrateguia_screen(page, nome)

    page.add(
        ft.Container(
            width=360,
            padding=18,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=14,
                controls=[
                    radar,
                    ft.Text("RADARTECH", size=34, weight=ft.FontWeight.BOLD, color=ft.Colors.CYAN_ACCENT_400),
                    ft.Container(
                        width=340,
                        padding=20,
                        border=ft.border.all(1.5, ft.Colors.with_opacity(0.5, ft.Colors.CYAN_ACCENT_400)),
                        border_radius=12,
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=8,
                            controls=[
                                ft.Text("MÉTRICA DE INTERESSE GLOBAL", size=12, color=ft.Colors.WHITE54),
                                ft.Text(
                                    "MATRIZ DE COMPETÊNCIA",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.WHITE,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                            ],
                        ),
                    ),
                    *barras,
                    ft.Text("Conexão Segura com SGBD | dados Anonimizados (LGPD)", size=9, color=ft.Colors.WHITE54),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=12,
                        controls=[
                            ft.TextButton("TENDÊNCIAS", on_click=abrir_tendencia),
                            ft.TextButton("PERFIS", on_click=lambda _: None),
                            ft.TextButton("ESTRATÉGIA", on_click=abrir_estrategia),
                        ],
                    ),
                ],
            ),
        )
    )
    page.update()

    async def animar_ponteiro_perfil() -> None:
        angulo = 0.0
        while True:
            try:
                if not page.controls:
                    break
                angulo += 0.08
                ponteiro.rotate = ft.Rotate(angulo, alignment=ft.alignment.Alignment(0, 0))
                page.update()
                await asyncio.sleep(0.03)
            except Exception:
                break

    page.run_task(animar_ponteiro_perfil)