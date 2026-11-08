"""
vv_manim.rotulos — Palabras de firma, paneles y cierres.

Convención de la casa: la prosa vive SOLO aquí — una palabra en Text/Georgia
que rotula lo que la geometría ya contó. Las fórmulas van en MathTex (M).
El cierre canónico de escena es firma(): palabra o fórmula + under_rule.
"""

from manim import *

from .theme import (
        INK,
        INK_SOFT,
        OXBLOOD,
        PAPER,
        under_rule,
)


def palabra(
        texto,
        scale=0.7,
        color=OXBLOOD,
):
    """Una palabra de firma, en Georgia. Úsala con cuentagotas."""
    rotulo = Text(
            texto,
            font="Georgia",
    ).scale(scale)
    rotulo.set_color(color)
    return rotulo


def panel(
        contenido,
        margen_x=0.7,
        margen_y=0.5,
        color=INK,
        fill=PAPER,
        opacity=0.9,
        corner=0.12,
        stroke=3,
):
    """Caja redondeada alrededor de un contenido (fórmula, alfabeto, cuenta).
    Devuelve VGroup(caja, contenido) ya agrupados y centrados."""
    caja = RoundedRectangle(
            corner_radius=corner,
            width=contenido.width + margen_x,
            height=contenido.height + margen_y,
            color=color,
            stroke_width=stroke,
            fill_color=fill,
            fill_opacity=opacity,
    )
    caja.move_to(contenido)

    return VGroup(
            caja,
            contenido,
    )


def firmar(
        scene,
        mob,
        escribir=True,
        run_time=0.8,
):
    """El cierre canónico: escribe (o aparece) el mob y traza su under_rule.
    'mob' es una palabra() o una fórmula M() ya posicionada."""
    if escribir:
        scene.play(
                Write(mob),
                run_time=run_time,
        )
    else:
        scene.play(
                FadeIn(
                        mob,
                        shift=UP * 0.2,
                ),
                run_time=run_time,
        )
    scene.play(
            Create(
                    under_rule(mob),
            ),
            run_time=0.5,
    )


def cabecera(
        texto,
        scale=0.45,
):
    """Rótulo discreto de columna o zona (sepia-suave, Georgia)."""
    rotulo = Text(
            texto,
            font="Georgia",
    ).scale(scale)
    rotulo.set_color(INK_SOFT)
    return rotulo
