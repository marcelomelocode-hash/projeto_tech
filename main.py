import asyncio
import flet as ft
from db import init_db

def main(page: ft.Page):
    try:
        init_db()
    except Exception as e:
        print(f"Erro ao inicializar banco: {e}")
    
    page.title = "Radar Tech - Carregando Sistema..."
    page.bgcolor = ft.Colors.BLACK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.width = 400
    page.window.height = 800

    from cadastroTech import criar_radar
    radar, pointer = criar_radar()

    titulo = ft.Text(
        value="RADARTECH",
        size=40,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.WHITE,
    )

    barra_carregamento = ft.ProgressBar(
        width=300,
        color=ft.Colors.CYAN_ACCENT_700,
        bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),
        value=0,
    )

    progresso_texto = ft.Text(
        value="Carregando... 0%",
        size=14,
        color=ft.Colors.WHITE70,
    )

    layout_loading = ft.Column(
        controls=[
            radar,
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            titulo,
            ft.Divider(height=40, color=ft.Colors.TRANSPARENT),
            barra_carregamento,
            progresso_texto,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    page.add(layout_loading)

    async def animar_loading():
        progresso = 0.0
        angulo = 0.0

        while progresso < 1:
            progresso = min(1, progresso + 0.02)
            barra_carregamento.value = progresso
            progresso_texto.value = f"Carregando... {int(progresso * 100)}%"

            angulo += 0.08
            pointer.rotate = ft.Rotate(angulo, alignment=ft.alignment.Alignment(0, 0))

            page.update()
            await asyncio.sleep(0.02)

        await asyncio.sleep(0.2)
        page.clean()
        
        from loginTech import show_login_screen
        show_login_screen(page)

    page.run_task(animar_loading)

if __name__ == "__main__":
    ft.app(target=main)
