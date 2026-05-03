import asyncio
import flet as ft
from cadastroTech import criar_radar


def show_estrateguia_screen(page: ft.Page, nome_usuario: str = "") -> None:
    page.clean()
    page.title = "Radar Tech - Estratégia"
    page.bgcolor = ft.Colors.BLACK
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    radar, ponteiro = criar_radar()
    nome = (nome_usuario or "RADARTECH").upper()

    c1 = ft.Checkbox(label="Coleta e tratamento de dados dos usuários", value=False, active_color=ft.Colors.CYAN_ACCENT_400)
    c2 = ft.Checkbox(
        label="Estudo de viabilidade (conforme indicadores: Tendências e perfis)",
        value=False,
        active_color=ft.Colors.YELLOW_400,
    )
    c3 = ft.Checkbox(
        label="Gerenciamento de projeto e adaptação às ferramentas ágeis corporativas",
        value=False,
        active_color=ft.Colors.CYAN_ACCENT_400,
    )
    progresso = ft.ProgressBar(value=0, width=280, color=ft.Colors.CYAN_ACCENT_400)
    progresso_texto = ft.Text("Progresso de Roadmap: 0%", size=10, color=ft.Colors.WHITE70)

    def atualizar_roadmap(_: ft.ControlEvent | None = None) -> None:
        total = 0.0
        if c1.value:
            total += 0.25
        if c2.value:
            total += 0.40
        if c3.value:
            total += 0.35

        percentual = int(round(total * 100))
        progresso.value = total
        progresso_texto.value = f"Progresso de Roadmap: {percentual}%"
        page.update()

    c1.on_change = atualizar_roadmap
    c2.on_change = atualizar_roadmap
    c3.on_change = atualizar_roadmap

    def abrir_tendencia(_: ft.ControlEvent) -> None:
        from tendencia import show_tendencia_screen
        show_tendencia_screen(page, nome)

    def abrir_perfil(_: ft.ControlEvent) -> None:
        from perfil import show_perfil_screen
        show_perfil_screen(page, nome)

    def sair_para_login(_: ft.ControlEvent) -> None:
        from loginTech import show_login_screen
        show_login_screen(page)

    page.add(
        ft.Container(
            width=360,
            padding=18,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=14,
                controls=[
                    radar,
                    ft.Text(nome, size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.Container(
                        width=320,
                        padding=14,
                        border=ft.border.all(1.2, ft.Colors.with_opacity(0.5, ft.Colors.CYAN_ACCENT_400)),
                        border_radius=10,
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Text("MÉTRICA DE INTERESSE GLOBAL", size=10, color=ft.Colors.WHITE54),
                                ft.Text(
                                    "PLANO DE EXPANSÃO TÉCNICA",
                                    size=22,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.WHITE,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                                ft.Text("DIRETRIZES ESTRATÉGICAS", size=12, color=ft.Colors.WHITE70),
                            ],
                        ),
                    ),
                    c1,
                    c2,
                    c3,
                    progresso_texto,
                    progresso,
                    ft.Text("Conexão Segura com SSL | Dados Anonimizados (LGPD)", size=9, color=ft.Colors.WHITE54),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=12,
                        controls=[
                            ft.TextButton("TENDÊNCIAS", on_click=abrir_tendencia),
                            ft.TextButton("PERFIS", on_click=abrir_perfil),
                            ft.TextButton("ESTRATÉGIA", on_click=lambda _: None),
                        ],
                    ),
                    ft.ElevatedButton(
                        "SAIR",
                        width=170,
                        on_click=sair_para_login,
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.CYAN_ACCENT_400,
                            color=ft.Colors.BLACK,
                            shape=ft.RoundedRectangleBorder(radius=28),
                        ),
                    ),
                ],
            ),
        )
    )
    atualizar_roadmap(None)

    async def animar_ponteiro() -> None:
        angulo = 0.0
        while True:
            angulo += 0.08
            ponteiro.rotate = ft.Rotate(angulo, alignment=ft.alignment.Alignment(0, 0))
            page.update()
            await asyncio.sleep(0.03)

    page.run_task(animar_ponteiro)
