"""
vv_manim.motores — El patrón motor: un updater invisible mueve el mundo.

Para animaciones que un Transform no puede contar (hélices que giran, mares
de glifos, profundidad por opacidad): un ValueTracker avanza una fase y un
VMobject invisible ("el motor") recoloca los objetos en cada frame.

Uso:
    fase = ValueTracker(0.0)

    def girar(_motor):
        avance = fase.get_value()
        ...  # recolocar objetos en función de 'avance'

    motor = encender_motor(scene, girar)
    scene.play(
            fase.animate.set_value(TAU),
            run_time=4.0,
            rate_func=linear,
    )
    apagar_motor(motor)
"""

from manim import *


def encender_motor(
        scene,
        actualizar,
):
    """Crea el motor invisible, le engancha el updater y lo añade a escena."""
    motor = VMobject()
    motor.add_updater(actualizar)
    scene.add(motor)
    return motor


def apagar_motor(motor):
    """Suelta los updaters. Llamar SIEMPRE al acabar: un motor vivo
    sigue recolocando objetos en las animaciones siguientes."""
    motor.clear_updaters()
    return motor


def profundidad(
        fase,
        minimo=0.45,
):
    """Pista de profundidad por opacidad: 1.0 delante, 'minimo' detrás.
    'fase' en radianes; delante = sin(fase) alto."""
    import numpy as np
    delante = 0.5 + 0.5 * np.sin(fase)
    return minimo + (1.0 - minimo) * delante
