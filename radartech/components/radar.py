import math
import flet as ft


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
                width=170,
                height=170,
                border=ft.Border.all(2, ft.Colors.CYAN_ACCENT_700),
                border_radius=85,
                shadow=ft.BoxShadow(
                    blur_radius=20,
                    color=ft.Colors.with_opacity(0.35, ft.Colors.CYAN_ACCENT_700),
                ),
            ),
            ft.Container(
                width=170,
                height=170,
                alignment=ft.alignment.Alignment(0, 0),
                content=ft.Container(
                    width=90,
                    height=90,
                    border=ft.Border.all(1.2, ft.Colors.with_opacity(0.55, ft.Colors.CYAN_ACCENT_400)),
                    border_radius=54,
                ),
            ),
            *linhas_grau,
            ponteiro,
            ft.Container(
                width=175,
                height=175,
                alignment=ft.alignment.Alignment(0, 0),
                content=ft.Container(
                    width=16,
                    height=16,
                    bgcolor=ft.Colors.CYAN_ACCENT_200,
                    border_radius=8,
                    shadow=ft.BoxShadow(blur_radius=16, color=ft.Colors.CYAN_ACCENT_200),
                ),
            ),
        ],
        width=175,
        height=175,
    )
    return radar, ponteiro

