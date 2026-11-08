"""
vv_manim.escalas — Reglas, ejes de potencias y tramos multiplicativos.

El gesto logarítmico hecho geometría: potencias a pasos IGUALES sobre una
regla, y el tramo que dice "x b" entre marca y marca. Sirve para cualquier
escala multiplicativa (dinero, decibelios, magnitudes, dígitos).
"""

from manim import *

from .theme import (
        INK,
        INK_SOFT,
        M,
        OXBLOOD,
        ink_line,
)


def escala_log(
        valores,
        largo=6.6,
        direccion=RIGHT,
        lado_etiqueta=UP,
        color=INK,
):
    """Regla logarítmica: los 'valores' (potencias) caen equiespaciados.
    Devuelve (VGroup(base, marcas), paso). Cada marca es VGroup(tick, etiqueta)."""
    n = len(valores)
    paso = largo / (n - 1)

    base = ink_line(
            -direccion * (largo / 2),
            direccion * (largo / 2),
            color=color,
            stroke_width=4,
    )

    #-- El tick es perpendicular a la dirección de la regla.
    normal = rotate_vector(
            direccion,
            PI / 2,
    )

    marcas = VGroup()
    for indice, valor in enumerate(valores):
        centro = -direccion * (largo / 2) + direccion * (indice * paso)
        tick = ink_line(
                centro - normal * 0.12,
                centro + normal * 0.12,
                color=color,
                stroke_width=3,
        )
        etiqueta = M(str(valor)).scale(0.5)
        etiqueta.next_to(
                tick,
                lado_etiqueta,
                buff=0.08,
        )
        marcas.add(
                VGroup(
                        tick,
                        etiqueta,
                ),
        )

    return VGroup(
            base,
            marcas,
    ), paso


def tramo_por(
        desde,
        hasta,
        factor_tex=r"\times 10",
        offset=DOWN * 0.35,
        color=OXBLOOD,
        lado_etiqueta=DOWN,
):
    """El tramo que dice 'x b': un trazo en acento entre dos puntos, rotulado.
    Devuelve VGroup(trazo, etiqueta)."""
    trazo = ink_line(
            desde + offset,
            hasta + offset,
            color=color,
            stroke_width=6,
    )
    etiqueta = M(factor_tex).scale(0.55)
    etiqueta.set_color(color)
    etiqueta.next_to(
            trazo,
            lado_etiqueta,
            buff=0.12,
    )

    return VGroup(
            trazo,
            etiqueta,
    )


def ejes_tinta(
        x_range,
        y_range,
        x_length,
        y_length,
):
    """Axes con el ajuste de tinta de la casa: sin ticks, punta pequeña."""
    return Axes(
            x_range=x_range,
            y_range=y_range,
            x_length=x_length,
            y_length=y_length,
            axis_config={
                    "color": INK_SOFT,
                    "stroke_width": 3,
                    "include_ticks": False,
                    "include_tip": True,
                    "tip_width": 0.18,
                    "tip_height": 0.18,
            },
    )
