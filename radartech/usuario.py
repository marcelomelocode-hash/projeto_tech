import flet as ft


def show_usuario_screen(page: ft.Page, nome_usuario: str) -> None:
    page.clean()
    page.title = "Radar Tech - Usuário"
    page.bgcolor = ft.Colors.BLACK
    page.scroll = ft.ScrollMode.AUTO

    nome = (nome_usuario or "USUÁRIO").strip().upper()

    page.add(
        ft.Container(
            expand=True,
            alignment=ft.alignment.Alignment(0, -1),
            content=ft.Container(
                width=360,
                padding=18,
                border=ft.border.all(1.5, ft.Colors.with_opacity(0.45, ft.Colors.CYAN_ACCENT_400)),
                border_radius=22,
                content=ft.Column(
                    spacing=12,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text("RADARTECH", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                        ft.Text("PERFIL DE INTERESSE", size=11, color=ft.Colors.CYAN_ACCENT_200),
                        ft.Text(nome, size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                        ft.Divider(height=8, color=ft.Colors.TRANSPARENT),
                        ft.Text("O QUE VOCÊ CURTE?", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                        ft.Text("Seleção de conteúdos e cursos", size=11, color=ft.Colors.WHITE70),
                        ft.ResponsiveRow(
                            controls=[
                                ft.Chip(label=ft.Text("Inteligência Artificial", color=ft.Colors.WHITE),
                                        bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.CYAN_ACCENT_700)),
                                ft.Chip(label=ft.Text("Desenvolvimento Web", color=ft.Colors.WHITE),
                                        bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.CYAN_ACCENT_700)),
                                ft.Chip(label=ft.Text("Linguagem de Programação", color=ft.Colors.WHITE),
                                        bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.CYAN_ACCENT_700)),
                                ft.Chip(label=ft.Text("UX/UI Design", color=ft.Colors.WHITE),
                                        bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.CYAN_ACCENT_700)),
                                ft.Chip(label=ft.Text("Cibersegurança", color=ft.Colors.WHITE),
                                        bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.CYAN_ACCENT_700)),
                                ft.Chip(label=ft.Text("Data Science", color=ft.Colors.WHITE),
                                        bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.CYAN_ACCENT_700)),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            run_spacing=6,
                            spacing=6,
                        ),
                        ft.Divider(height=8, color=ft.Colors.TRANSPARENT),
                        ft.Text("⭐ SELECIONE VIP", size=13, color=ft.Colors.AMBER_200),
                        ft.Container(
                            width=290,
                            padding=12,
                            border=ft.border.all(1.2, ft.Colors.CYAN_ACCENT_400),
                            border_radius=12,
                            content=ft.Column(
                                spacing=4,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Text("Aula 01: O futuro da IA no Design", color=ft.Colors.WHITE, size=13),
                                    ft.Text("Conteúdo premium exclusivo VIP", color=ft.Colors.WHITE70, size=11),
                                ],
                            ),
                        ),
                        ft.Text("MATERIAIS EXCLUSIVOS", size=27, weight=ft.FontWeight.BOLD, color=ft.Colors.CYAN_ACCENT_200),
                        ft.OutlinedButton("E-book: Guia de Carreira em UX/UI", width=290),
                        ft.OutlinedButton("Checklist: Heurísticas de UX", width=290),
                        ft.Container(height=6),
                        ft.ElevatedButton(
                            "SAIR",
                            width=170,
                            style=ft.ButtonStyle(
                                bgcolor=ft.Colors.CYAN_ACCENT_400,
                                color=ft.Colors.BLACK,
                                shape=ft.RoundedRectangleBorder(radius=28),
                            ),
                            on_click=lambda _: page.window.close(),
                        ),
                    ],
                ),
            ),
        )
    )
    page.update()
