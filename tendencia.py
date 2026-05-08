import asyncio
import flet as ft
from cadastroTech import criar_radar
from dados_mock import top_n_interesses


def show_tendencia_screen(page: ft.Page, nome_usuario: str = "") -> None:
    page.clean()
    page.title = "Radar Tech - Tendências"
    page.bgcolor = ft.Colors.BLACK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO

    radar, ponteiro = criar_radar()
    nome = (nome_usuario or "RADARTECH").upper()

    top_cursos = top_n_interesses(5)
    barras: list[ft.Container] = []
    altura_total = 180
    largura_barra = 42

    for idx, (curso, votos, percentual) in enumerate(top_cursos):
        altura_fill = max(12, int((percentual / 100) * altura_total))
        nome_vertical = "\n".join(list(curso[:18]))

        barras.append(
            ft.Container(
                width=largura_barra,
                height=altura_total,
                bgcolor=ft.Colors.with_opacity(0.18, ft.Colors.CYAN_ACCENT_200),
                border=ft.border.all(1, ft.Colors.with_opacity(0.5, ft.Colors.CYAN_ACCENT_400)),
                border_radius=14,
                alignment=ft.alignment.Alignment(0, 1),
                clip_behavior=ft.ClipBehavior.HARD_EDGE,
                tooltip=f"{curso}: {votos} votos ({percentual:.1f}%)",
                content=ft.Container(
                    width=largura_barra,
                    height=altura_fill,
                    bgcolor=ft.Colors.CYAN_ACCENT_400 if idx == 0 else ft.Colors.with_opacity(0.52, ft.Colors.CYAN_ACCENT_400),
                    border_radius=14,
                    alignment=ft.alignment.Alignment(0, 0),
                    padding=ft.padding.symmetric(horizontal=2, vertical=4),
                    content=ft.Text(
                        nome_vertical,
                        size=8,
                        color=ft.Colors.BLACK,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                        max_lines=18,
                        overflow=ft.TextOverflow.CLIP,
                    ),
                ),
            )
        )

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
                    ft.Text(
                        "RADARTECH",
                        size=34,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.CYAN_ACCENT_400,
                    ),
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
