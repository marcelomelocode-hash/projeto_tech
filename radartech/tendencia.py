import asyncio
import flet as ft
from cadastroTech import criar_radar


def show_tendencia_screen(page: ft.Page, nome_usuario: str = "") -> None:
    page.clean()
    page.title = "Radar Tech - Tendências"
    page.bgcolor = ft.Colors.BLACK
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    radar, ponteiro = criar_radar()
    nome = (nome_usuario or "RADARTECH").upper()

    # Dados iniciais das barras (serão alimentados por outro código futuramente)
    valores_barras = [0.82, 0.62, 0.55, 0.48, 0.41]
    barras = [
        ft.Container(
            width=12,
            height=130,
            bgcolor=ft.Colors.with_opacity(0.25, ft.Colors.CYAN_ACCENT_200),
            border_radius=8,
            alignment=ft.alignment.Alignment(0, 1),
            content=ft.Container(
                width=12,
                height=max(10, int(130 * valor)),
                bgcolor=ft.Colors.CYAN_ACCENT_400 if i == 0 else ft.Colors.with_opacity(0.45, ft.Colors.CYAN_ACCENT_400),
                border_radius=8,
            ),
        )
        for i, valor in enumerate(valores_barras)
    ]

    def abrir_perfil(_: ft.ControlEvent) -> None:
        from perfil import show_perfil_screen
        show_perfil_screen(page, nome)

    def abrir_estrategia(_: ft.ControlEvent) -> None:
        from estrategia import show_estrateguia_screen
        show_estrateguia_screen(page, nome)

    page.add(
        ft.Container(
            width=360,
            padding=18,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=16,
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
                                    "MÉTRICAS DE CRESCIMENTO",
                                    size=20,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.WHITE,
                                    text_align=ft.TextAlign.CENTER,
                                    no_wrap=True,
                                ),
                            ],
                        ),
                    ),
                    ft.Row(alignment=ft.MainAxisAlignment.CENTER, spacing=12, controls=barras),
                    ft.Text("Conexão Segura com SGBD | dados anonimizados (LGPD)", size=9, color=ft.Colors.WHITE54),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=12,
                        controls=[
                            ft.TextButton("TENDÊNCIAS", on_click=lambda _: None),
                            ft.TextButton("PERFIS", on_click=abrir_perfil),
                            ft.TextButton("ESTRATÉGIA", on_click=abrir_estrategia),
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
