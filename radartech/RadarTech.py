import asyncio
import flet as ft
from loginTech import show_login_screen
from cadastroTech import criar_radar


# Função principal da aplicação.
# Recebe o objeto Page do Flet para montar e controlar toda a interface.
def main(page: ft.Page):
    # =========================
    # Configuração geral da janela
    # =========================
    # Título mostrado na aba/janela durante a tela de carregamento.
    page.title = "Radar Tech - Loading..."
    # Cor de fundo principal da aplicação.
    page.bgcolor = ft.Colors.BLACK
    # Largura da janela (simulando proporção de celular).
    page.window_width = 400
    # Altura da janela (simulando proporção de celular).
    page.window_height = 800
    # Alinhamento vertical padrão dos controles da página.
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    # Alinhamento horizontal padrão dos controles da página.
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Radar igual ao da tela de login.
    radar, ponteiro = criar_radar()

    # Título principal da tela de carregamento.
    titulo = ft.Text(
        value="RADARTECH",
        size=40,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.WHITE,
    )

    # Barra de progresso que será preenchida de 0% até 100%.
    barra_carregamento = ft.ProgressBar(
        width=300,
        color=ft.Colors.CYAN_ACCENT_700,
        bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),
        # Inicia vazia.
        value=0,
    )

    # Texto que mostra a porcentagem atual do carregamento.
    progresso_texto = ft.Text(
        value="Carregando... 0%",
        size=14,
        color=ft.Colors.WHITE70,
    )

    # =========================
    # Layout da primeira tela (loading)
    # =========================
    # Layout da tela de loading com radar + título + barra.
    layout_loading = ft.Column(
        controls=[
            # Radar animado.
            radar,
            # Espaçamento entre radar e título.
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            # Texto da marca.
            titulo,
            # Espaçamento entre título e barra.
            ft.Divider(height=40, color=ft.Colors.TRANSPARENT),
            # Barra de carregamento.
            barra_carregamento,
            # Texto da porcentagem.
            progresso_texto,
        ],
        # Centralização horizontal dos elementos.
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # Exibe layout de loading ao iniciar app.
    page.add(layout_loading)

    # =========================
    # Lógica de animação
    # =========================
    # Coroutine responsável por animar barra + ponteiro.
    async def animar_loading():
        # Progresso inicial da barra.
        progresso = 0.0
        # Ângulo inicial do ponteiro.
        angulo = 0.0

        # Loop de animação até completar 100%.
        while progresso < 1:
            # Incrementa progresso gradualmente.
            progresso = min(1, progresso + 0.01)
            # Atualiza valor visual da barra.
            barra_carregamento.value = progresso
            # Atualiza texto com percentual inteiro.
            progresso_texto.value = f"Carregando... {int(progresso * 100)}%"

            # Incrementa rotação do ponteiro a cada frame.
            # O valor em radianos cresce continuamente para gerar rotação.
            angulo += 0.08
            # Aplica nova rotação (pivô no centro do radar).
            ponteiro.rotate = ft.Rotate(angulo, alignment=ft.alignment.Alignment(0, 0))

            # Re-renderiza a interface com novos valores.
            page.update()
            # Intervalo curto para suavidade da animação.
            await asyncio.sleep(0.03)

        # Pequena pausa ao atingir 100%.
        await asyncio.sleep(0.3)
        # Troca para a tela de login após o loading.
        show_login_screen(page)

    # Dispara a animação assíncrona sem bloquear a UI principal.
    page.run_task(animar_loading)


# Inicializa app Flet e abre no navegador padrão.
ft.app(target=main, view=ft.AppView.WEB_BROWSER)
