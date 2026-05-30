import flet as ft
import asyncio
from db import get_db_connection


def _criar_wrapped_rows(items: list, controls_per_row: int = 2) -> list[ft.Row]:
    rows = []
    for i in range(0, len(items), controls_per_row):
        chunk = items[i:i + controls_per_row]
        rows.append(
            ft.Row(
                controls=chunk,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
                wrap=True,
            )
        )
    return rows


def show_interesse_screen(page: ft.Page) -> None:
    page.clean()
    page.title = "Radar Tech - Interesses"
    page.bgcolor = ft.Colors.BLACK
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO

    from cadastroTech import criar_radar
    radar, ponteiro = criar_radar()

    try:
        usuario_email = page.session.get("user_email")
    except Exception:
        from db import get_session_store
        usuario_email = get_session_store().get("user_email")

    jornada_selecionada = [None]
    interesses_selecionados = set()

    status_erro = ft.Text(value="", color=ft.Colors.RED_ACCENT_400, size=12)

    def _atualizar_cor_botao(btn, selecionado: bool):
        if selecionado:
            btn.bgcolor = ft.Colors.CYAN_ACCENT_400
            btn.color = ft.Colors.BLACK
            if btn.content and isinstance(btn.content, ft.Text):
                btn.content.color = ft.Colors.BLACK
        else:
            btn.bgcolor = ft.Colors.TRANSPARENT
            btn.color = ft.Colors.CYAN_ACCENT_400
            if btn.content and isinstance(btn.content, ft.Text):
                btn.content.color = ft.Colors.CYAN_ACCENT_400

    def selecionar_jornada(e):
        valor = e.control.data
        for btn in botoes_jornada:
            _atualizar_cor_botao(btn, False)
        _atualizar_cor_botao(e.control, True)
        jornada_selecionada[0] = valor
        page.update()

    def alternar_interesse(e):
        valor = e.control.data
        if valor in interesses_selecionados:
            interesses_selecionados.remove(valor)
            _atualizar_cor_botao(e.control, False)
        else:
            interesses_selecionados.add(valor)
            _atualizar_cor_botao(e.control, True)
        page.update()

    def salvar_dados(e):
        if not usuario_email:
            status_erro.value = "Erro: Usuário não identificado na sessão."
            page.update()
            return

        if not jornada_selecionada[0]:
            status_erro.value = "Por favor, selecione seu momento da jornada."
            page.update()
            return

        if not interesses_selecionados:
            status_erro.value = "Por favor, selecione pelo menos um interesse."
            page.update()
            return

        str_interesses = ", ".join(interesses_selecionados)

        try:
            conexao = get_db_connection(include_database=True)
            cursor = conexao.cursor()
            cursor.execute(
                "UPDATE tbl_cadastro SET jornada = %s, interesses = %s WHERE email_usuario = %s",
                (jornada_selecionada[0], str_interesses, usuario_email)
            )
            conexao.commit()
            cursor.close()
            conexao.close()

            status_erro.value = "Dados salvos com sucesso! Redirecionando..."
            status_erro.color = ft.Colors.GREEN_ACCENT_200
            page.update()

            from loginTech import show_login_screen
            show_login_screen(page)
        except Exception as err:
            status_erro.value = f"Erro ao salvar interesses: {err}"
            page.update()

    opcoes_jornada = [
        "Entusiasta / Curioso", "Estudante / Iniciante",
        "Profissional Júnior", "Profissional Pleno / Sênior",
        "Liderança / Gestão"
    ]
    botoes_jornada = []
    for op in opcoes_jornada:
        btn = ft.ElevatedButton(
            data=op,
            on_click=selecionar_jornada,
            style=ft.ButtonStyle(
                color=ft.Colors.CYAN_ACCENT_400,
                bgcolor=ft.Colors.TRANSPARENT,
                shape=ft.RoundedRectangleBorder(radius=15),
                side=ft.BorderSide(1, ft.Colors.CYAN_ACCENT_400),
            ),
        )
        btn.content = ft.Text(op, size=12, color=ft.Colors.CYAN_ACCENT_400)
        botoes_jornada.append(btn)

    opcoes_interesses = [
        "Como desenvolver sua própria IA", "C++",
        "Curso de C#", "Desenvolvimento Web",
        "Java", "Lógica de Programação",
        "Machine Learning", "Python", "SQL",
        "Segurança da Informação", "UI/UX Design"
    ]
    botoes_interesses = []
    for op in opcoes_interesses:
        btn = ft.ElevatedButton(
            data=op,
            on_click=alternar_interesse,
            style=ft.ButtonStyle(
                color=ft.Colors.CYAN_ACCENT_400,
                bgcolor=ft.Colors.TRANSPARENT,
                shape=ft.RoundedRectangleBorder(radius=15),
                side=ft.BorderSide(1, ft.Colors.CYAN_ACCENT_400),
            ),
        )
        btn.content = ft.Text(op, size=12, color=ft.Colors.CYAN_ACCENT_400)
        botoes_interesses.append(btn)

    linhas_jornada = _criar_wrapped_rows(botoes_jornada, 2)
    linhas_interesses = _criar_wrapped_rows(botoes_interesses, 2)

    page.add(
        ft.Container(
            padding=ft.padding.only(top=20, bottom=40),
            content=ft.Column(
                controls=[
                    radar,
                    ft.Text("RADARTECH", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.CYAN_ACCENT_400),
                    ft.Text("Jornada do Usuário", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.Text("Em qual momento você está?", size=12, color=ft.Colors.WHITE54),
                    *linhas_jornada,
                    ft.Container(height=10),
                    ft.Text("O QUE VOCÊ CURTE?", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.Text("Seleção de Conteúdo", size=12, color=ft.Colors.WHITE54),
                    *linhas_interesses,
                    ft.Container(height=15),
                    ft.ElevatedButton(
                        "CADASTRAR",
                        on_click=salvar_dados,
                        bgcolor=ft.Colors.CYAN_ACCENT_400,
                        color=ft.Colors.BLACK,
                        width=300,
                        height=45,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=28),
                            text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD),
                        ),
                    ),
                    status_erro,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=12,
            ),
        )
    )
    page.update()

    async def animar_ponteiro_interesse() -> None:
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

    page.run_task(animar_ponteiro_interesse)