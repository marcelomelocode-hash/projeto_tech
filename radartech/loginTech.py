import flet as ft
import asyncio
from cadastroTech import criar_radar, show_cadastro_screen, USUARIO_TESTE_CADASTRO
from tendencia import show_tendencia_screen

def show_login_screen(page: ft.Page) -> None:
    page.clean()
    page.title = "Radar Tech - Login"
    page.bgcolor = ft.Colors.BLACK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO

    # Inicialização do Radar
    radar, ponteiro = criar_radar()

    # Configuração dos Campos de Texto
    usuario = ft.TextField(
        label="Usuário(email)",
        width=300,
        color=ft.Colors.WHITE,
        border_color=ft.Colors.CYAN_ACCENT_400,
        focused_border_color=ft.Colors.CYAN_ACCENT_200,
    )
    
    senha = ft.TextField(
        label="Senha",
        password=True,
        can_reveal_password=True,
        width=300,
        color=ft.Colors.WHITE,
        border_color=ft.Colors.CYAN_ACCENT_400,
        focused_border_color=ft.Colors.CYAN_ACCENT_200,
    )

    status = ft.Text(value="", size=14)

    def entrar(_: ft.ControlEvent) -> None:
        # Validação com dados preenchidos em cadastroTech.py
        usuario_cadastrado = (USUARIO_TESTE_CADASTRO.get("usuario") or "").strip()
        senha_cadastrada = (USUARIO_TESTE_CADASTRO.get("senha") or "").strip()

        if usuario.value == usuario_cadastrado and senha.value == senha_cadastrada and usuario_cadastrado and senha_cadastrada:
            status.value = "Acesso autorizado! Carregando..."
            status.color = ft.Colors.GREEN_ACCENT_400
            page.update()
            
            show_tendencia_screen(page, "RADARTECH")
        
        elif not usuario.value or not senha.value:
            status.value = "Por favor, preencha todos os campos"
            status.color = ft.Colors.RED_300
        elif not usuario_cadastrado or not senha_cadastrada:
            status.value = "Cadastre-se primeiro para liberar o acesso"
            status.color = ft.Colors.RED_300
        else:
            status.value = "Usuário ou senha incorretos"
            status.color = ft.Colors.RED_300
        
        page.update()

    def abrir_cadastro(_: ft.ControlEvent) -> None:
        show_cadastro_screen(page)

    telefone_recuperacao = ft.TextField(
        label="Número de telefone",
        hint_text="(DDD) 99999-9999",
        width=320,
        color=ft.Colors.WHITE,
        border_color=ft.Colors.CYAN_ACCENT_400,
    )

    whatsapp_recuperacao = ft.Checkbox(
        value=False,
        label="Desejo que reencaminhe minha senha pelo WhatsApp",
        label_style=ft.TextStyle(size=12, color=ft.Colors.WHITE70),
        active_color=ft.Colors.CYAN_ACCENT_400,
    )

    status_recuperacao = ft.Text(value="", size=12, color=ft.Colors.WHITE70)

    def abrir_recuperacao_senha(_: ft.ControlEvent) -> None:
        telefone_recuperacao.value = ""
        whatsapp_recuperacao.value = False
        status_recuperacao.value = ""

        def enviar_recuperacao(__: ft.ControlEvent) -> None:
            if not telefone_recuperacao.value or not telefone_recuperacao.value.strip():
                status_recuperacao.value = "Informe o número de telefone para continuar"
                status_recuperacao.color = ft.Colors.RED_300
                page.update()
                return

            canal = "WhatsApp" if whatsapp_recuperacao.value else "SMS"
            status_recuperacao.value = f"Solicitação enviada. Reenvio da senha via {canal}."
            status_recuperacao.color = ft.Colors.GREEN_ACCENT_200
            page.update()

        dialogo = ft.AlertDialog(
            modal=True,
            bgcolor=ft.Colors.BLACK,
            title=ft.Text("Recuperar senha", color=ft.Colors.CYAN_ACCENT_200),
            content=ft.Column(
                tight=True,
                spacing=10,
                controls=[
                    telefone_recuperacao,
                    whatsapp_recuperacao,
                    status_recuperacao,
                ],
            ),
            actions=[
                ft.TextButton(
                    "Cancelar",
                    on_click=lambda e: (
                        setattr(dialogo, "open", False),
                        page.update(),
                    ),
                ),
                ft.ElevatedButton(
                    "Enviar",
                    on_click=enviar_recuperacao,
                    bgcolor=ft.Colors.CYAN_ACCENT_400,
                    color=ft.Colors.BLACK,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.dialog = dialogo
        dialogo.open = True
        page.update()

    usuario.on_submit = entrar
    senha.on_submit = entrar

    # Montagem da Interface (Layout)
    page.add(
        ft.Column(
            controls=[
                radar,
                ft.Text(
                    "RADARTECH", 
                    size=34, 
                    weight=ft.FontWeight.BOLD, 
                    color=ft.Colors.CYAN_ACCENT_400 # Título em Ciano para combinar com o radar
                ),
                ft.Container(height=10),
                usuario,
                senha,
                ft.Container(height=10),
                # Botão Entrar customizado com as cores do radar
                ft.ElevatedButton(
                    "ENTRAR", 
                    on_click=entrar, 
                    bgcolor=ft.Colors.CYAN_ACCENT_400, 
                    color=ft.Colors.BLACK, 
                    width=300,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
                ),
                # Botão de Cadastro
                ft.TextButton(
                    "Novo por aqui? Criar conta", 
                    on_click=abrir_cadastro,
                    style=ft.ButtonStyle(color=ft.Colors.CYAN_ACCENT_700)
                ),
                ft.TextButton(
                    content=ft.Text("Esqueci minha senha", size=12),
                    on_click=abrir_recuperacao_senha,
                    width=300,
                    style=ft.ButtonStyle(
                        color=ft.Colors.CYAN_ACCENT_200,
                        shape=ft.RoundedRectangleBorder(radius=8),
                    ),
                ),
                status,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        )
    )
    
    page.update()

    # Animação do Ponteiro (Executa em background)
    async def animar_ponteiro_login() -> None:
        angulo = 0.0
        while True:
            try:
                angulo += 0.08
                ponteiro.rotate = ft.Rotate(angulo, alignment=ft.alignment.Alignment(0, 0))
                page.update()
                await asyncio.sleep(0.03)
            except Exception:
                break # Para a animação se mudar de página

    page.run_task(animar_ponteiro_login)
