import asyncio
import flet as ft
from cadastroTech import criar_radar

def show_interesse_screen(page: ft.Page) -> None:
    page.clean()
    page.title = "Radar Tech - Interesses"
    page.bgcolor = ft.Colors.BLACK
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO

    # Recupera o radar do arquivo de cadastro
    radar, ponteiro = criar_radar()

    jornada_opcoes = [
        "Entusiasta / Curioso",
        "Estudante / Iniciante",
        "Profissional Júnior",
        "Profissional Pleno / Sênior",
        "Liderança / Gestão",
    ]

    curso_opcoes = [
        "Como desenvolver sua própria IA",
        "C++",
        "Curso de C#",
        "Desenvolvimento Web",
        "Java",
        "Lógica de Programação",
        "Machine Learning",
        "Python",
        "SQL",
        "Segurança da Informação",
        "UI/UX Design",
    ]

    selecionado_jornada: dict[str, str | None] = {"valor": None}
    selecionado_curso: dict[str, str | None] = {"valor": None}

    status = ft.Text(value="", size=13, color=ft.Colors.RED_300)

    botoes_jornada: list[ft.OutlinedButton] = []
    botoes_curso: list[ft.OutlinedButton] = []

    def estilo_box(ativo: bool) -> ft.ButtonStyle:
        return ft.ButtonStyle(
            side=ft.BorderSide(2, ft.Colors.CYAN_ACCENT_400),
            shape=ft.RoundedRectangleBorder(radius=18),
            bgcolor=ft.Colors.CYAN_ACCENT_400 if ativo else ft.Colors.TRANSPARENT,
            color=ft.Colors.BLACK if ativo else ft.Colors.CYAN_ACCENT_200,
            padding=ft.Padding(12, 10, 12, 10),
        )

    def atualizar_botoes() -> None:
        for botao in botoes_jornada:
            ativo = botao.data == selecionado_jornada["valor"]
            botao.style = estilo_box(ativo)
            if isinstance(botao.content, ft.Text):
                botao.content.color = ft.Colors.BLACK if ativo else ft.Colors.CYAN_ACCENT_200
        
        for botao in botoes_curso:
            ativo = botao.data == selecionado_curso["valor"]
            botao.style = estilo_box(ativo)
            if isinstance(botao.content, ft.Text):
                botao.content.color = ft.Colors.BLACK if ativo else ft.Colors.CYAN_ACCENT_200
        
        page.update()

    def selecionar_jornada(e: ft.ControlEvent) -> None:
        selecionado_jornada["valor"] = e.control.data
        atualizar_botoes()

    def selecionar_curso(e: ft.ControlEvent) -> None:
        selecionado_curso["valor"] = e.control.data
        atualizar_botoes()

    # Criação dos botões usando 'content' para compatibilidade
    for opcao in jornada_opcoes:
        botoes_jornada.append(
            ft.OutlinedButton(
                content=ft.Text(opcao, color=ft.Colors.CYAN_ACCENT_200),
                data=opcao,
                on_click=selecionar_jornada,
                style=estilo_box(False),
            )
        )

    for opcao in curso_opcoes:
        botoes_curso.append(
            ft.OutlinedButton(
                content=ft.Text(opcao, color=ft.Colors.CYAN_ACCENT_200),
                data=opcao,
                on_click=selecionar_curso,
                style=estilo_box(False),
            )
        )

    def cadastrar(_: ft.ControlEvent) -> None:
        if not selecionado_jornada["valor"]:
            status.value = "Selecione 1 opção da Jornada do Usuário"
            page.update()
            return

        if not selecionado_curso["valor"]:
            status.value = "Selecione 1 opção em O que você curte"
            page.update()
            return

        status.value = "Cadastro concluído com sucesso"
        status.color = ft.Colors.GREEN_ACCENT_200
        page.update()

        from loginTech import show_login_screen
        show_login_screen(page)

    # Layout Principal
    page.add(
        ft.Container(
            width=360,
            padding=ft.padding.only(top=24, bottom=24, left=14, right=14),
            content=ft.Column(
                spacing=14,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    radar,
                    ft.Text("RADARTECH", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.CYAN_ACCENT_200),
                    ft.Text("Jornada do Usuário", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.Text("Em qual momento você está?", size=12, color=ft.Colors.WHITE70),
                    
                    # SUBSTITUIÇÃO DO WRAP PELO ROW COM WRAP=TRUE
                    ft.Row(
                        controls=botoes_jornada,
                        wrap=True,
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=8,
                        run_spacing=8,
                    ),
                    
                    ft.Text("O QUE VOCÊ CURTE?", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.Text("Seleção de Conteúdo", size=12, color=ft.Colors.WHITE70),
                    
                    # SUBSTITUIÇÃO DO WRAP PELO ROW COM WRAP=TRUE
                    ft.Row(
                        controls=botoes_curso,
                        wrap=True,
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=8,
                        run_spacing=8,
                    ),
                    
                    ft.Container(height=14),
                    ft.ElevatedButton(
                        content=ft.Text("CADASTRAR", weight=ft.FontWeight.BOLD),
                        on_click=cadastrar,
                        bgcolor=ft.Colors.CYAN_ACCENT_400,
                        color=ft.Colors.BLACK,
                        width=300,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=14)),
                    ),
                    status,
                ],
            ),
        )
    )

    page.update()

    async def animar_ponteiro_interesse() -> None:
        angulo = 0.0
        while True:
            try:
                # Verifica se a página ainda existe para evitar erro ao trocar de tela
                if not page.controls: break
                angulo += 0.08
                ponteiro.rotate = ft.Rotate(angulo, alignment=ft.alignment.Alignment(0, 0))
                page.update()
                await asyncio.sleep(0.03)
            except:
                break

    page.run_task(animar_ponteiro_interesse)
