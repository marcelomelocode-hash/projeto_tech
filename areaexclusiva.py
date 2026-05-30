import flet as ft
import asyncio

from cadastroTech import criar_radar
from cadastroTech import show_cadastro_screen, USUARIO_TESTE_CADASTRO
from conexao import conectar, fechar_conexao

HISTORICO_USUARIO: list[dict[str, str]] = []


def show_area_exclusiva_screen(page: ft.Page, jornada: str, curso: str, id_usuario: int = 1) -> None:
    page.clean()
    page.title = "Radar Tech - Área Exclusiva"
    page.bgcolor = ft.Colors.BLACK
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    radar, ponteiro = criar_radar()
    HISTORICO_USUARIO.append({"jornada": jornada, "curso": curso})

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

    def abrir_atualizar_cadastro(_: ft.ControlEvent) -> None:
        def salvar_alteracoes(_: ft.ControlEvent) -> None:
            if not txt_nome.value or not txt_telefone.value:
                page.snack_bar = ft.SnackBar(ft.Text("Por favor, preencha todos os campos!"))
                page.snack_bar.open = True
                page.update()
                return
            
            conexao = conectar()
            if conexao:
                cursor = conexao.cursor()
                try:
                    cursor.execute(
                        """UPDATE tbl_cadastro 
                           SET nome_completo = %s, telefone_usuario = %s 
                           WHERE id_cadastro = %s""",
                        (txt_nome.value, txt_telefone.value, id_usuario)
                    )
                    conexao.commit()
                    dialogo_edicao.open = False
                    page.snack_bar = ft.SnackBar(ft.Text("Cadastro atualizado com sucesso no MySQL!"))
                    page.snack_bar.open = True
                    page.update()
                except Exception as erro:
                    print("Erro ao atualizar dados no banco:", erro)
                finally:
                    cursor.close()
                    fechar_conexao(conexao)

        txt_nome = ft.TextField(label="Novo Nome Completo", color=ft.Colors.WHITE)
        txt_telefone = ft.TextField(label="Novo Telefone", color=ft.Colors.WHITE)

        dialogo_edicao = ft.AlertDialog(
            title=ft.Text("Atualizar Dados Cadastrais", color=ft.Colors.WHITE),
            content=ft.Column([txt_nome, txt_telefone], tight=True),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: setattr(dialogo_edicao, 'open', False) or page.update()),
                ft.ElevatedButton("Salvar", on_click=salvar_alteracoes, bgcolor=ft.Colors.CYAN_ACCENT_400, color=ft.Colors.BLACK)
            ],
            bgcolor=ft.Colors.GREY_900
        )
        page.overlay.append(dialogo_edicao)
        dialogo_edicao.open = True
        page.update()

    def excluir_dados_cadastrais(_: ft.ControlEvent) -> None:
        def confirmar_exclusao(_: ft.ControlEvent) -> None:
            conexao = conectar()
            if conexao:
                cursor = conexao.cursor()
                try:
                    cursor.execute("DELETE FROM tbl_usuario_cursos WHERE cadastro_id = %s", (id_usuario,))
                    cursor.execute("DELETE FROM tbl_cadastro WHERE id_cadastro = %s", (id_usuario,))
                    
                    conexao.commit()
                    
                    HISTORICO_USUARIO.clear()
                    USUARIO_TESTE_CADASTRO["usuario"] = ""
                    USUARIO_TESTE_CADASTRO["senha"] = ""

                    dialogo_confirmacao.open = False
                    page.snack_bar = ft.SnackBar(ft.Text("Dados pessoais totalmente removidos do sistema."))
                    page.snack_bar.open = True

                    from loginTech import show_login_screen
                    show_login_screen(page)
                except Exception as erro:
                    print("Erro ao excluir do banco de dados:", erro)
                finally:
                    cursor.close()
                    fechar_conexao(conexao)

        dialogo_confirmacao = ft.AlertDialog(
            title=ft.Text("Confirmar Exclusão", color=ft.Colors.WHITE),
            content=ft.Text("Deseja mesmo apagar suas informações do banco de dados de forma definitiva?", color=ft.Colors.WHITE),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: setattr(dialogo_confirmacao, 'open', False) or page.update()),
                ft.ElevatedButton("Confirmar Exclusão", on_click=confirmar_exclusao, bgcolor=ft.Colors.RED_ACCENT_400, color=ft.Colors.WHITE)
            ],
            bgcolor=ft.Colors.GREY_900
        )
        page.overlay.append(dialogo_confirmacao)
        dialogo_confirmacao.open = True
        page.update()

    box_atualizar = ft.Container(
        width=182,
        padding=10,
        border_radius=10,
        bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.CYAN_ACCENT_400),
        ink=True,
        on_click=abrir_atualizar_cadastro,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
            controls=[
                ft.Icon(ft.Icons.EDIT_DOCUMENT, color=ft.Colors.CYAN_ACCENT_200, size=13),
                ft.Text(
                    "atualizar dados cadastrais",
                    color=ft.Colors.WHITE,
                    size=9,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
        ),
    )

    box_excluir = ft.Container(
        width=182,
        padding=10,
        border_radius=10,
        bgcolor=ft.Colors.with_opacity(0.08, ft.Colors.RED_400),
        ink=True,
        on_click=excluir_dados_cadastrais,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
            controls=[
                ft.Icon(ft.Icons.DELETE_FOREVER, color=ft.Colors.RED_ACCENT_100, size=13),
                ft.Text(
                    "excluir dados cadastrais",
                    color=ft.Colors.WHITE,
                    size=9,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
        ),
    )

    box_atualizar_interesse = ft.Container(
        width=182,
        padding=10,
        border_radius=10,
        bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.CYAN_ACCENT_400),
        ink=True,
        on_click=atualizar_interesse,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
            controls=[
                ft.Icon(ft.Icons.TUNE, color=ft.Colors.CYAN_ACCENT_200, size=13),
                ft.Text(
                    "atualizar interesse",
                    color=ft.Colors.WHITE,
                    size=9,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
        ),
    )

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
                    f"Curso: {curso}",
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
                                height=96,
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
                            ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=8,
                                controls=[
                                    box_atualizar,
                                    box_excluir,
                                ],
                            ),
                            box_atualizar_interesse,
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