"""
vv_manim.casillas — Casillas de dígito, filas, giros y marcadores.

La familia de patrones más reutilizada del canal: una casilla contiene un
símbolo; una fila de casillas escribe un número; las casillas giran como un
marcador mecánico; un marcador de tinta invertida hace de odómetro.

Convención de ritmo: los pasos intermedios de un giro son rápidos; el valor
final se sostiene (hold) para dar tiempo a leerlo.
"""

from manim import *

from .theme import (
        INK,
        M,
        OXBLOOD,
        PAPER,
        PAPER_DEEP,
)


# ----------------------------------------------------------------------------
# Construcción
# ----------------------------------------------------------------------------

def digit_box(
        tex,
        width=0.62,
        height=0.78,
        color=INK,
        fill=PAPER_DEEP,
        opacity=0.55,
        stroke=3,
):
    """Una casilla: caja redondeada + símbolo centrado. box[0]=caja, box[1]=valor."""
    box = RoundedRectangle(
            corner_radius=0.06,
            width=width,
            height=height,
            color=color,
            stroke_width=stroke,
            fill_color=fill,
            fill_opacity=opacity,
    )
    value = M(str(tex)).scale(0.86)
    value.set_color(color)
    value.move_to(box)

    return VGroup(
            box,
            value,
    )


def digit_row(
        digits,
        scale=1.0,
        buff=0.08,
        color=INK,
):
    """Una fila de casillas (un número escrito en un alfabeto)."""
    row = VGroup(
            *[
                    digit_box(
                            digit,
                            color=color,
                    )
                    for digit in digits
            ],
    )
    row.arrange(
            RIGHT,
            buff=buff,
    )
    row.scale(scale)

    return row


def resaltar_casilla(
        box,
        color=OXBLOOD,
        stroke=5,
):
    """Devuelve la animación que convierte una casilla en protagonista."""
    return AnimationGroup(
            box[0].animate.set_stroke(
                    color=color,
                    width=stroke,
            ),
            box[1].animate.set_color(color),
    )


def marcador(
        valores,
        buff=0.35,
):
    """Odómetro de tinta invertida: dígitos de papel sobre cuerpo de tinta.
    marcador[0]=cuerpo, marcador[1]=ruedas (VGroup), marcador[2]=marco."""
    n_ruedas = len(valores)
    cuerpo = RoundedRectangle(
            corner_radius=0.16,
            width=0.95 * n_ruedas + 0.4,
            height=1.6,
            stroke_width=0,
            fill_color=INK,
            fill_opacity=1.0,
    )
    ruedas = VGroup(
            *[
                    M(str(v), color=PAPER).scale(1.3)
                    for v in valores
            ],
    )
    ruedas.arrange(
            RIGHT,
            buff=buff,
    )
    ruedas.move_to(cuerpo)

    marco = RoundedRectangle(
            corner_radius=0.16,
            width=cuerpo.width,
            height=cuerpo.height,
            color=PAPER,
            stroke_width=3,
            fill_opacity=0.0,
    )
    marco.move_to(cuerpo)

    return VGroup(
            cuerpo,
            ruedas,
            marco,
    )


# ----------------------------------------------------------------------------
# Animación
# ----------------------------------------------------------------------------

def set_box_value(
        box,
        tex,
):
    """La animación que cambia el símbolo de una casilla."""
    new_value = M(str(tex)).scale(0.86)
    new_value.move_to(box[0])

    return Transform(
            box[1],
            new_value,
    )


def spin_box(
        scene,
        box,
        values,
        pace=0.34,
        hold=0.55,
):
    """La casilla gira por varios valores, como un marcador mecánico.
    El último valor se sostiene para que se pueda leer."""
    for indice, value in enumerate(values):
        es_ultimo = indice == len(values) - 1
        scene.play(
                set_box_value(
                        box,
                        value,
                ),
                run_time=pace,
        )
        if es_ultimo:
            scene.wait(hold)


def spin_boxes(
        scene,
        boxes,
        secuencias,
        pace=0.30,
        hold=0.6,
):
    """Varias casillas giran A LA VEZ (más vivo en un marcador).
    'secuencias': una lista de valores por casilla; pueden tener largos distintos."""
    n_pasos = max(len(seq) for seq in secuencias)
    for paso in range(n_pasos):
        animaciones = []
        for box, seq in zip(boxes, secuencias):
            if paso < len(seq):
                animaciones.append(
                        set_box_value(
                                box,
                                seq[paso],
                        ),
                )
        scene.play(
                *animaciones,
                run_time=pace,
        )
    scene.wait(hold)
