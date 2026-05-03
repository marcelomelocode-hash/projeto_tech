import asyncio
import flet as ft
from cadastroTech import criar_radar


def show_perfil_screen(page: ft.Page, nome_usuario: str = "") -> None:
    page.clean()
    page.title = "Radar Tech - Perfis"
    page.bgcolor = ft.Colors.BLACK
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO

    radar, ponteiro = criar_radar()
    nome = (nome_usuario or "RADARTECH").upper()

    opcoes = [
        "Entusiasta / Curioso",
        "Estudante / Iniciante",
        "Profissional Júnior",
        "Profissional Pleno/Sênior",
        "Liderança / Gestão",
    ]
    perfil_selecionado = {"valor": None}

    def selecionar_perfil(valor: str):
        def _selecionar(_: ft.ControlEvent) -> None:
            perfil_selecionado["valor"] = valor
            page.update()

        return _selecionar

    boxes_perfil = [
        ft.Container(
            width=320,
            padding=ft.padding.symmetric(horizontal=14, vertical=12),
            border=ft.border.all(1.2, ft.Colors.with_opacity(0.55, ft.Colors.CYAN_ACCENT_400)),
            border_radius=22,
            bgcolor=ft.Colors.with_opacity(0.12, ft.Colors.CYAN_ACCENT_400),
            ink=True,
            on_click=selecionar_perfil(txt),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
                controls=[
                    ft.Container(
                        width=12,
                        height=12,
                        border_radius=6,
                        border=ft.border.all(1.5, ft.Colors.WHITE70),
                        bgcolor=ft.Colors.with_opacity(0.15, ft.Colors.WHITE),
                    ),
                    ft.Text(txt, color=ft.Colors.WHITE, size=13),
                ],
            ),
        )
        for txt in opcoes
    ]

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
                                    "MATRIZ DE COMPETÊNCIA",
                                    size=20,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.WHITE,
                                    text_align=ft.TextAlign.CENTER,
                                    no_wrap=True,
                                ),
                            ],
                        ),
                    ),
                    *boxes_perfil,
                    ft.Text("Conexão segura com SGBD | dados Anonimizados (LGPD)", size=9, color=ft.Colors.WHITE54),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=12,
                        controls=[
                            ft.OutlinedButton("TENDÊNCIAS", on_click=abrir_tendencia),
                            ft.OutlinedButton("PERFIS", on_click=lambda _: None),
                            ft.OutlinedButton("ESTRATÉGIA", on_click=abrir_estrategia),
                        ],
                    ),
                ],
            ),
        )
    )
    page.update()

    async def animar_ponteiro() -> None:
        angulo = 0.0
        while True:
            angulo += 0.08
            ponteiro.rotate = ft.Rotate(angulo, alignment=ft.alignment.Alignment(0, 0))
            page.update()
            await asyncio.sleep(0.03)

    page.run_task(animar_ponteiro)
