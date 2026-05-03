import flet as ft
import asyncio

from cadastroTech import criar_radar


def show_area_exclusiva_screen(page: ft.Page, jornada: str, curso: str) -> None:
    page.clean()
    page.title = "Radar Tech - Área Exclusiva"
    page.bgcolor = ft.Colors.BLACK
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    radar, ponteiro = criar_radar()

    links_video = {
        "Como desenvolver sua própria IA": "https://www.youtube.com/watch?v=aircAruvnKk",
        "C++": "https://www.youtube.com/watch?v=vLnPwxZdW4Y",
        "Curso de C#": "https://www.youtube.com/watch?v=GhQdlIFylQ8",
        "Desenvolvimento Web": "https://www.youtube.com/watch?v=UB1O30fR-EE",
        "Java": "https://www.youtube.com/watch?v=grEKMHGYyns",
        "Lógica de Programação": "https://www.youtube.com/watch?v=8mei6uVttho",
        "Machine Learning": "https://www.youtube.com/watch?v=ukzFI9rgwfU",
        "Python": "https://www.youtube.com/watch?v=_uQrJ0TkZlc",
        "SQL": "https://www.youtube.com/watch?v=HXV3zeQKqGY",
        "Segurança da Informação": "https://www.youtube.com/watch?v=inWWhr5tnEA",
        "UI/UX Design": "https://www.youtube.com/watch?v=c9Wg6Cb_YlU",
    }

    nivel_texto = {
        "Entusiasta / Curioso": "Aula 01: Uma IA exclusiva",
        "Estudante / Iniciante": "Aula 01: Fundamentos do curso escolhido",
        "Profissional Júnior": "Aula 01: Aplicações práticas e carreira",
        "Profissional Pleno / Sênior": "Aula 01: Escala, arquitetura e boas práticas",
        "Liderança / Gestão": "Aula 01: Estratégia, impacto e visão de negócio",
    }

    def abrir_video(_: ft.ControlEvent) -> None:
        page.launch_url(links_video.get(curso, "https://www.youtube.com"))

    def abrir_ebook(_: ft.ControlEvent) -> None:
        page.snack_bar = ft.SnackBar(ft.Text(f"Em breve: e-book exclusivo para {jornada} em {curso}."))
        page.snack_bar.open = True
        page.update()

    def abrir_checklist(_: ft.ControlEvent) -> None:
        page.snack_bar = ft.SnackBar(ft.Text(f"Em breve: checklist e curiosidades de {curso}."))
        page.snack_bar.open = True
        page.update()

    def sair(_: ft.ControlEvent) -> None:
        from loginTech import show_login_screen

        show_login_screen(page)

    def atualizar_interesse(_: ft.ControlEvent) -> None:
        from interesseTech import show_interesse_screen

        show_interesse_screen(page)

    card_aula = ft.Container(
        width=250,
        padding=16,
        border=ft.border.all(1.8, ft.Colors.CYAN_ACCENT_400),
        border_radius=12,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
            controls=[
                ft.IconButton(
                    icon=ft.Icons.ARROW_DROP_DOWN,
                    icon_color=ft.Colors.CYAN_ACCENT_400,
                    icon_size=44,
                    on_click=abrir_video,
                    tooltip="Assistir vídeo na própria jornada",
                ),
                ft.Text(
                    nivel_texto.get(jornada, "Aula 01: Conteúdo exclusivo"),
                    size=11,
                    color=ft.Colors.WHITE,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    "Curso: XXXX",
                    size=10,
                    color=ft.Colors.WHITE70,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
        ),
    )

    page.add(
        ft.Container(
            width=360,
            padding=ft.padding.only(top=18, left=12, right=12, bottom=18),
            content=ft.Stack(
                controls=[
                    ft.Column(
                        spacing=12,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            radar,
                            ft.Text("RADARTECH", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.CYAN_ACCENT_200),
                            ft.Divider(color=ft.Colors.WHITE24),
                            ft.Text("Jornada do Usuário", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                            card_aula,
                            ft.Text("MATERIAIS EXCLUSIVOS", size=12, color=ft.Colors.CYAN_ACCENT_400, weight=ft.FontWeight.BOLD),
                            ft.OutlinedButton(
                                content=ft.Text("E-book: Da calculadora à IA"),
                                on_click=abrir_ebook,
                                width=260,
                                style=ft.ButtonStyle(
                                    side=ft.BorderSide(1.5, ft.Colors.CYAN_ACCENT_400),
                                    color=ft.Colors.WHITE,
                                    shape=ft.RoundedRectangleBorder(radius=8),
                                ),
                            ),
                            ft.OutlinedButton(
                                content=ft.Column(
                                    spacing=2,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        ft.Text("(lógica pedagógica): modulo Neutron -> Mapa atômico de [interesse]", text_align=ft.TextAlign.CENTER),
                                        ft.Text(
                                            "Neutron do conhecimento a cada quebra de conceito particulas menores de subconceitos até chegar no conhecimento pratico",
                                            size=6,
                                            weight=ft.FontWeight.BOLD,
                                            color=ft.Colors.CYAN_ACCENT_200,
                                            text_align=ft.TextAlign.CENTER,
                                        ),
                                    ],
                                ),
                                on_click=abrir_checklist,
                                width=260,
                                icon=ft.Icons.OPEN_IN_NEW,
                                style=ft.ButtonStyle(
                                    side=ft.BorderSide(1.5, ft.Colors.CYAN_ACCENT_400),
                                    color=ft.Colors.WHITE,
                                    shape=ft.RoundedRectangleBorder(radius=8),
                                ),
                            ),
                            ft.Container(height=80),
                            ft.ElevatedButton(
                                "SAIR",
                                on_click=sair,
                                bgcolor=ft.Colors.CYAN_ACCENT_400,
                                color=ft.Colors.BLACK,
                                width=130,
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=18)),
                            ),
                            ft.TextButton(
                                content=ft.Text("Atualizar Interesse", size=11, color=ft.Colors.WHITE54),
                                on_click=atualizar_interesse,
                                style=ft.ButtonStyle(
                                    overlay_color=ft.Colors.with_opacity(0.08, ft.Colors.CYAN_ACCENT_400),
                                ),
                            ),
                        ],
                    ),
                ]
            ),
        )
    )

    page.update()

    async def animar_ponteiro_area_exclusiva() -> None:
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

    page.run_task(animar_ponteiro_area_exclusiva)

