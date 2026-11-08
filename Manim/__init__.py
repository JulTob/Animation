"""
vv_manim — Librería de animación de Vilo Vitae para Manim.

Tinta sobre papel, formato vertical, sin prosa. Cuatro módulos por idea de uso:

    theme     paleta, portrait()/landscape(), InkScene, M, accent, under_rule
    casillas  casillas de dígito, filas, giros de marcador, odómetro
    rotulos   palabras de firma (Georgia), paneles, el cierre firmar()
    escalas   reglas logarítmicas, tramos x b, ejes de tinta
    motores   el patrón motor (updater invisible) para animación continua

Uso típico en un archivo de escenas:

    from manim import *
    from vv_manim.theme import *
    from vv_manim.casillas import digit_row, spin_boxes
    from vv_manim.rotulos import palabra, firmar

    portrait()
"""

from .theme import (
        DUSK_BLUE,
        FADE_GREEN,
        FRAME_H,
        FRAME_W,
        INK,
        INK_SOFT,
        InkScene,
        M,
        OXBLOOD,
        OXBLOOD_DK,
        PAPER,
        PAPER_DEEP,
        SEPIA,
        accent,
        ink_line,
        landscape,
        portrait,
        soft_brace,
        under_rule,
)
