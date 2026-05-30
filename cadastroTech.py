import math
import flet as ft
import asyncio
import re
import mysql.connector  
from db import get_db_connection

USUARIO_TESTE_CADASTRO: dict[str, str] = {"usuario": "", "senha": ""}

def criar_radar() -> tuple[ft.Stack, ft.Container]:
    linhas_grau = [
        ft.Container(
            width=170,
            height=170,
            alignment=ft.alignment.Alignment(0, -1),
            content=ft.Container(
                width=1,
                height=10 if grau % 30 == 0 else 6,
                bgcolor=ft.Colors.with_opacity(
                    0.55 if grau % 30 == 0 else 0.28,
                    ft.Colors.CYAN_ACCENT_200,
                ),
                border_radius=1,
            ),
            rotate=ft.Rotate(math.radians(grau), alignment=ft.alignment.Alignment(0, 0)),
        )
        for grau in range(0, 360, 10)
    ]

    ponteiro = ft.Container(
        width=170,
        height=170,
        alignment=ft.alignment.Alignment(0, -1),
        content=ft.Container(
            width=26,
            height=84,
            alignment=ft.alignment.Alignment(0, -1),
            content=ft.Column(
                spacing=0,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        width=2,
                        height=72,
                        bgcolor=ft.Colors.CYAN_ACCENT_400,
                        border_radius=2,
                        shadow=ft.BoxShadow(blur_radius=8, color=ft.Colors.CYAN_ACCENT_700),
                    ),
                ],
            ),
        ),
        rotate=ft.Rotate(0, alignment=ft.alignment.Alignment(0, 0)),
        animate_rotation=ft.Animation(90, curve=ft.AnimationCurve.LINEAR),
    )

    radar = ft.Stack(
        controls=[
            ft.Container(
                width=170, height=170,
                border=ft.Border.all(2, ft.Colors.CYAN_ACCENT_700),
                border_radius=85,
                shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.with_opacity(0.35, ft.Colors.CYAN_ACCENT_700)),
            ),
            ft.Container(
                width=170, height=170,
                alignment=ft.alignment.Alignment(0, 0),
                content=ft.Container(
                    width=90, height=90,
                    border=ft.Border.all(1.2, ft.Colors.with_opacity(0.55, ft.Colors.CYAN_ACCENT_400)),
                    border_radius=54,
                ),
            ),
            *linhas_grau,
            ponteiro,
            ft.Container(
                width=175, height=175,
                alignment=ft.alignment.Alignment(0, 0),
                content=ft.Container(
                    width=16, height=16,
                    bgcolor=ft.Colors.CYAN_ACCENT_200,
                    border_radius=8,
                    shadow=ft.BoxShadow(blur_radius=16, color=ft.Colors.CYAN_ACCENT_200),
                ),
            ),
        ],
        width=175, height=175,
    )
    return radar, ponteiro

def show_cadastro_screen(page: ft.Page) -> None:
    page.clean()
    page.title = "Radar Tech - Cadastro"
    page.bgcolor = "#000000"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO

    radar, ponteiro = criar_radar()

    titulo = ft.Text("RADARTECH", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.CYAN_ACCENT_200)
    subtitulo = ft.Text("CRIE SUA CONTA", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)

    nome = ft.TextField(label="Nome completo", width=320, color=ft.Colors.WHITE, border_color=ft.Colors.CYAN_ACCENT_400, on_change=lambda e: atualizar_progresso())
    email = ft.TextField(label="E-mail", width=320, color=ft.Colors.WHITE, border_color=ft.Colors.CYAN_ACCENT_400, on_change=lambda e: atualizar_progresso())
    ddd = ft.TextField(label="DDD", width=90, color=ft.Colors.WHITE, border_color=ft.Colors.CYAN_ACCENT_400, on_change=lambda e: atualizar_progresso())
    telefone = ft.TextField(label="Telefone", width=220, color=ft.Colors.WHITE, border_color=ft.Colors.CYAN_ACCENT_400, on_change=lambda e: atualizar_progresso())
    senha = ft.TextField(label="Senha", password=True, can_reveal_password=True, width=320, color=ft.Colors.WHITE, border_color=ft.Colors.CYAN_ACCENT_400, on_change=lambda e: atualizar_progresso())
    confirmar_senha = ft.TextField(label="Confirmar senha", password=True, can_reveal_password=True, width=320, color=ft.Colors.WHITE, border_color=ft.Colors.CYAN_ACCENT_400, on_change=lambda e: atualizar_progresso())

    aceitar_termos = ft.Checkbox(
        value=False,
        label="Ao acessar, você concorda com nossos Termos de Uso e Políticas de Privacidade (LGPD)",
        label_style=ft.TextStyle(size=10, color=ft.Colors.WHITE54),
        active_color=ft.Colors.CYAN_ACCENT_400,
        on_change=lambda e: atualizar_progresso()
    )
    
    status = ft.Text(value="", color=ft.Colors.RED_300)
    progresso_texto = ft.Text("Complete o cadastro: 0%", size=10, color=ft.Colors.WHITE70)
    barra_progresso = ft.ProgressBar(width=300, value=0, color=ft.Colors.CYAN_ACCENT_400, bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.WHITE))

    redirecionando = {"ok": False}

    def validar_campos() -> tuple[list[bool], bool]:
        nome_ok = bool(nome.value and len(nome.value.strip().split()) >= 2)
        email_valor = (email.value or "").strip().lower()
        email_ok = bool(email_valor and "@" in email_valor)
        email_radar = email_valor.startswith("radar")

        ddd_valor = re.sub(r"\D", "", ddd.value or "")
        ddd_ok = len(ddd_valor) == 2
        tel_valor = re.sub(r"\D", "", telefone.value or "")
        telefone_ok = ddd_ok and len(tel_valor) >= 8

        senha_valor = senha.value or ""
        if email_radar:
            senha_ok = bool(senha_valor.strip())
        else:
            senha_ok = bool(len(senha_valor) >= 5 and re.search(r"\d", senha_valor) and re.search(r"[^A-Za-z0-9]", senha_valor))

        confirmar_ok = bool(confirmar_senha.value and confirmar_senha.value == senha_valor)
        termos_ok = True if email_radar else bool(aceitar_termos.value)

        return [nome_ok, email_ok, telefone_ok, senha_ok, confirmar_ok, termos_ok], email_radar

    def obter_pendencias(itens: list[bool], email_radar: bool) -> list[str]:
        pendencias = []
        if not itens[0]: pendencias.append("Nome e Sobrenome")
        if not itens[1]: pendencias.append("E-mail válido")
        if not itens[2]: pendencias.append("Telefone completo")
        if not itens[3] and not email_radar: pendencias.append("Senha forte")
        if not itens[4]: pendencias.append("Senhas iguais")
        if not itens[5] and not email_radar: pendencias.append("Aceitar termos")
        return pendencias

    def atualizar_progresso(_: ft.ControlEvent | None = None) -> None:
        itens, email_radar = validar_campos()
        progresso = sum(itens) / len(itens)
        percentual = int(progresso * 100)
        
        barra_progresso.value = progresso
        progresso_texto.value = f"Complete o cadastro: {percentual}%"

        if percentual < 100:
            redirecionando["ok"] = False
            pendencias = obter_pendencias(itens, email_radar)
            status.value = "Pendências: " + " | ".join(pendencias) if percentual > 0 else ""
            status.color = ft.Colors.WHITE54
            status.size = 10
            page.update()
        elif not redirecionando["ok"]:
            redirecionando["ok"] = True
            status.value = "100% - Salvando no MySQL e avançando..."
            status.color = ft.Colors.GREEN_ACCENT_200
            status.size = 14
            page.update()
            
            email_cadastro = email.value.strip().lower()
            USUARIO_TESTE_CADASTRO["usuario"] = email_cadastro
            USUARIO_TESTE_CADASTRO["senha"] = senha.value.strip()

            try:
                page.session.set("user_email", email_cadastro)
            except Exception:
                from db import get_session_store
                get_session_store().set("user_email", email_cadastro)

            telefone_completo = f"({re.sub(r'\D', '', ddd.value or '')}){re.sub(r'\D', '', telefone.value or '')}"
            
            try:
                conexao = get_db_connection(include_database=True)
                cursor = conexao.cursor()
                
                cursor.execute("SELECT id_cadastro FROM tbl_cadastro WHERE email_usuario = %s", (email_cadastro,))
                if cursor.fetchone():
                    status.value = "Este e-mail já está cadastrado."
                    status.color = ft.Colors.RED_ACCENT_400
                    redirecionando["ok"] = False
                    page.update()
                    cursor.close()
                    conexao.close()
                    return

                cursor.execute(
                    """INSERT INTO tbl_cadastro 
                    (nome_completo, email_usuario, telefone_usuario, senha_usuario, aceitar_termos, curso) 
                    VALUES (%s, %s, %s, %s, %s, %s)""",
                    (nome.value.strip(), email_cadastro, telefone_completo, senha.value.strip(), 1 if aceitar_termos.value else 0, "Python"),
                )
                conexao.commit()
                cursor.close()
                conexao.close()

                if email_cadastro.startswith("radar"):
                    from tendencia import show_tendencia_screen
                    show_tendencia_screen(page, "RADARTECH")
                else:
                    from interesseTech import show_interesse_screen
                    show_interesse_screen(page)

            except Exception as err:
                status.value = f"Erro no Banco: {err}"
                status.color = ft.Colors.RED_ACCENT_400
                redirecionando["ok"] = False
                page.update()

    page.add(
        ft.Container(
            padding=ft.padding.only(top=40, bottom=40),
            content=ft.Column(
                controls=[
                    radar, titulo, subtitulo, ft.Container(height=10),
                    nome, email,
                    ft.Row(controls=[ddd, telefone], alignment=ft.MainAxisAlignment.CENTER, width=320),
                    senha, confirmar_senha, ft.Container(content=aceitar_termos, width=320),
                    ft.Container(height=10), barra_progresso, progresso_texto, status
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15
            )
        )
    )
    page.update()

    async def animar_radar_cadastro() -> None:
        angulo = 0.0
        while True:
            try:
                if not page.controls: break
                angulo += 0.08
                ponteiro.rotate = ft.Rotate(angulo, alignment=ft.alignment.Alignment(0, 0))
                page.update()
                await asyncio.sleep(0.03)
            except Exception: break

    page.run_task(animar_radar_cadastro)