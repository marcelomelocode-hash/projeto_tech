import flet as ft
import asyncio
import re
from components.radar import criar_radar

# Dicionário global para simular persistência temporária
USUARIO_TESTE_CADASTRO: dict[str, str] = {"usuario": "", "senha": ""}

def show_cadastro_screen(page: ft.Page) -> None:
    page.clean()
    page.title = "Radar Tech - Cadastro"
    page.bgcolor = "#000000"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO

    radar, ponteiro = criar_radar()

    # UI Elements
    titulo = ft.Text("RADARTECH", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.CYAN_ACCENT_200)
    subtitulo = ft.Text("CRIE SUA CONTA", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)

    nome = ft.TextField(label="Nome completo", width=320, color=ft.Colors.WHITE, border_color=ft.Colors.CYAN_ACCENT_400)
    email = ft.TextField(label="E-mail", width=320, color=ft.Colors.WHITE, border_color=ft.Colors.CYAN_ACCENT_400)
    ddd = ft.TextField(label="DDD", width=90, color=ft.Colors.WHITE, border_color=ft.Colors.CYAN_ACCENT_400)
    telefone = ft.TextField(label="Telefone", width=220, color=ft.Colors.WHITE, border_color=ft.Colors.CYAN_ACCENT_400)
    senha = ft.TextField(label="Senha", width=320, password=True, can_reveal_password=True, color=ft.Colors.WHITE, border_color=ft.Colors.CYAN_ACCENT_400)
    confirmar_senha = ft.TextField(label="Confirmar senha", width=320, password=True, can_reveal_password=True, color=ft.Colors.WHITE, border_color=ft.Colors.CYAN_ACCENT_400)

    aceitar_termos = ft.Checkbox(
        value=False,
        label="Ao acessar, você concorda com nossos Termos de Uso e Políticas de Privacidade (LGPD)",
        label_style=ft.TextStyle(size=10, color=ft.Colors.WHITE54),
        active_color=ft.Colors.CYAN_ACCENT_400,
    )
    
    status = ft.Text(value="", color=ft.Colors.RED_300)
    progresso_texto = ft.Text("Complete o cadastro: 0%", size=10, color=ft.Colors.WHITE70)
    barra_progresso = ft.ProgressBar(width=300, value=0, color=ft.Colors.CYAN_ACCENT_400, bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.WHITE))

    redirecionando = {"ok": False}

    def validar_campos() -> tuple[list[bool], list[str], bool]:
        # Validação Nome
        nome_ok = bool(nome.value and len(nome.value.strip().split()) >= 2)
        
        # Validação E-mail e Detecção de Prefixo "radar"
        email_valor = (email.value or "").strip().lower()
        email_ok = bool(email_valor and "@" in email_valor)
        email_radar = email_valor.startswith("radar")

        # Validação Telefone
        ddd_valor = re.sub(r"\D", "", ddd.value or "")
        ddd_ok = len(ddd_valor) == 2
        tel_valor = re.sub(r"\D", "", telefone.value or "")
        telefone_ok = ddd_ok and len(tel_valor) >= 8

        # Validação Senha (Flexível para radar)
        senha_valor = senha.value or ""
        if email_radar:
            senha_ok = bool(senha_valor.strip())
        else:
            senha_ok = bool(len(senha_valor) >= 5 and re.search(r"\d", senha_valor) and re.search(r"[^A-Za-z0-9]", senha_valor))

        confirmar_ok = bool(confirmar_senha.value and confirmar_senha.value == senha_valor)
        termos_ok = True if email_radar else bool(aceitar_termos.value)

        itens = [nome_ok, email_ok, telefone_ok, senha_ok, confirmar_ok, termos_ok]
        
        pendencias = []
        if not nome_ok: pendencias.append("Nome e Sobrenome")
        if not email_ok: pendencias.append("E-mail válido")
        if not ddd_ok or not telefone_ok: pendencias.append("Telefone completo")
        if not senha_ok and not email_radar: pendencias.append("Senha forte")
        if not confirmar_ok: pendencias.append("Senhas iguais")
        if not termos_ok and not email_radar: pendencias.append("Aceitar termos")

        return itens, pendencias, email_radar

    def atualizar_progresso(_: ft.ControlEvent | None = None) -> None:
        itens, pendencias, email_radar = validar_campos()
        progresso = sum(itens) / len(itens)
        percentual = int(progresso * 100)
        
        barra_progresso.value = progresso
        progresso_texto.value = f"Complete o cadastro: {percentual}%"

        if percentual < 100:
            redirecionando["ok"] = False
            status.value = "Pendências: " + " | ".join(pendencias) if percentual > 0 else ""
            status.color = ft.Colors.WHITE54
            status.size = 10
        elif not redirecionando["ok"]:
            redirecionando["ok"] = True
            status.value = "100% - Processando integração..."
            status.color = ft.Colors.GREEN_ACCENT_200
            status.size = 14
            # Grava dados e inicia fluxo de saída
            USUARIO_TESTE_CADASTRO["usuario"] = email.value.strip()
            USUARIO_TESTE_CADASTRO["senha"] = senha.value.strip()
            page.run_task(processar_redirecionamento)

        page.update()

    async def processar_redirecionamento() -> None:
        await asyncio.sleep(1.0) # Delay para feedback visual
        email_valor = (email.value or "").strip().lower()
        
        if email_valor.startswith("radar"):
            try:
                # INTEGRACAO COM INTERESSE TECH
                from interesseTech import show_interesse_screen
                show_interesse_screen(page)
            except Exception as e:
                status.value = f"Erro ao abrir interesseTech.py: {e}"
                status.color = ft.Colors.RED_400
                page.update()
        else:
            # FLUXO COMUM
            from loginTech import show_login_screen
            show_login_screen(page)

    # Eventos de mudança
    for field in [nome, email, ddd, telefone, senha, confirmar_senha]:
        field.on_change = atualizar_progresso
    aceitar_termos.on_change = atualizar_progresso

    def voltar_login(_: ft.ControlEvent) -> None:
        from loginTech import show_login_screen
        show_login_screen(page)

    # Montagem da tela
    page.add(
        ft.Container(
            width=360,
            padding=ft.padding.all(20),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
                controls=[
                    radar, titulo, subtitulo,
                    nome, email,
                    ft.Row([ddd, telefone], spacing=10, alignment=ft.MainAxisAlignment.CENTER),
                    senha, confirmar_senha,
                    ft.Row([ft.Text("Já tem uma conta?", color="white70"), ft.TextButton("Entrar", on_click=voltar_login)], alignment=ft.MainAxisAlignment.CENTER),
                    aceitar_termos,
                    barra_progresso, progresso_texto,
                    status
                ]
            )
        )
    )
    
    # Animação do Radar
    async def animar_radar():
        angulo = 0
        while True:
            angulo += 0.1
            ponteiro.rotate = ft.Rotate(angulo, alignment=ft.alignment.Alignment(0, 0))
            page.update()
            await asyncio.sleep(0.03)

    page.run_task(animar_radar)

# Se estiver rodando este arquivo diretamente para teste:
if __name__ == "__main__":
    def main(page: ft.Page):
        show_cadastro_screen(page)
    ft.app(target=main)
