# Animation

# vv_manim

Librería de animación de **Vilo Vitae** para [Manim Community](https://www.manim.community/):
tinta sobre papel, formato vertical, sin prosa. Los principios y patrones están
en la [wiki del repo](../../wiki/Manim), capítulo Manim.

## Instalación

Desde la raíz del repo, en el venv del proyecto que anima:

```bash
pip install -e ./manim
```

O, sin instalar, añadiendo la ruta (estilo legado de los proyectos del canal):

```python
import sys
sys.path.insert(0, "/ruta/a/Animation/manim")
```

## Uso mínimo

```python
from manim import *
from vv_manim.theme import *
from vv_manim.casillas import digit_row, spin_boxes
from vv_manim.rotulos import palabra, firmar

portrait()   # vertical 1080x1920, tinta por defecto. ANTES de las clases.


class MiEscena(InkScene):

    def construct(self):
        fila = digit_row(["1", "0", "0"])
        self.play(FadeIn(fila))

        cierre = palabra("casillas")
        cierre.move_to(DOWN * 5.0)
        firmar(self, cierre)
```

## Módulos (por idea de uso, no por tipo)

| Módulo | Qué contiene |
|---|---|
| `theme` | paleta, `portrait()`/`landscape()`, `InkScene`, `M`, `accent`, `under_rule`, `soft_brace` |
| `casillas` | `digit_box`, `digit_row`, `spin_box(es)`, `marcador` (odómetro), `resaltar_casilla` |
| `rotulos` | `palabra` (Georgia), `panel`, `firmar` (cierre canónico), `cabecera` |
| `escalas` | `escala_log`, `tramo_por` (×b), `ejes_tinta` |
| `motores` | `encender_motor` / `apagar_motor` (patrón updater), `profundidad` |

## Textura de papel (opcional)

Si existe `vv_manim/assets/paper_bg.png`, `InkScene` la pone de fondo.
Sin ella, el color `PAPER` basta: nada se rompe.

## Calidad y previews

Variables de entorno (las lee `portrait()`/`landscape()`):

```bash
VV_SCALE=0.5 manim -ql escenas.py MiEscena    # preview rápida
VV_SCALE=2.0 VV_FPS=60 VV_CRF=16 manim -qk escenas.py MiEscena   # máster 4K
```
