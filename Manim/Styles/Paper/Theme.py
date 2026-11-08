"""
vv_manim.theme — La estética compartida: tinta sobre papel / academia ligera.

Paleta: tinta carbón sobre papel hueso, con UN acento (oxblood desaturado).
Formato: vertical 1080x1920 (Shorts / TikTok) por defecto.
Regla de oro: sin prosa — las escenas hablan con matemáticas, geometría
infográfica y, como mucho, una palabra de firma.

Origen: consolidado de manim_999/theme.py (Vilo Vitae).
"""

from manim import *
import manim.scene.scene_file_writer as scene_file_writer
import os

# ----------------------------------------------------------------------------
# Paleta
# ----------------------------------------------------------------------------
PAPER      = "#EFE6D2"   # papel hueso (fondo)
PAPER_DEEP = "#E4D8BE"   # papel hundido: sombras suaves y rellenos
INK        = "#1C1B18"   # tinta carbón (negro cálido)
INK_SOFT   = "#403B31"   # tinta suave: marcas secundarias
SEPIA      = "#6B5B47"   # sepia: ticks, de-énfasis
OXBLOOD    = "#880000"   # EL acento. Solo para el protagonista de la escena.
OXBLOOD_DK = "#5E0808"
FADE_GREEN = "#586B4C"   # verde academia (opcional)
DUSK_BLUE  = "#3C4A5A"   # azul crepúsculo (opcional)

# ----------------------------------------------------------------------------
# Geometría / archivos
# ----------------------------------------------------------------------------
ASSET_DIR = os.path.join(os.path.dirname(__file__), "assets")
PAPER_BG  = os.path.join(ASSET_DIR, "paper_bg.png")

#-- Vertical 9:16. ~8 unidades de ancho para que las ecuaciones respiren.
FRAME_W = 8.0
FRAME_H = FRAME_W * (1920.0 / 1080.0)   # = 14.2222...


def portrait():
    """Configura Manim para el short vertical + tinta por defecto.
    Llamar ANTES de definir las clases de escena.

    Variables de entorno para iterar rápido:
      VV_SCALE  factor de escala de píxel (0.5 previews; 1.0 = 1080x1920)
      VV_FPS    frame rate (30 para revisar; 60 para el máster final)
      VV_CRF    CRF de x264 para másters de subida (p. ej. 16)
    """
    scale = float(os.environ.get("VV_SCALE", "1.0"))
    config.pixel_width  = int(round(1080 * scale))
    config.pixel_height = int(round(1920 * scale))
    config.frame_rate   = float(os.environ.get("VV_FPS", "30"))
    config.frame_width  = FRAME_W
    config.frame_height = FRAME_H
    config.background_color = PAPER

    for klass in (MathTex, Tex):
        klass.set_default(color=INK)
    Text.set_default(
            color=INK,
            font="Georgia",
    )
    apply_crf_override()


def landscape():
    """Variante 16:9 (vídeos largos). Misma tinta, lienzo horizontal."""
    scale = float(os.environ.get("VV_SCALE", "1.0"))
    config.pixel_width  = int(round(1920 * scale))
    config.pixel_height = int(round(1080 * scale))
    config.frame_rate   = float(os.environ.get("VV_FPS", "30"))
    config.frame_width  = FRAME_H
    config.frame_height = FRAME_W
    config.background_color = PAPER

    for klass in (MathTex, Tex):
        klass.set_default(color=INK)
    Text.set_default(
            color=INK,
            font="Georgia",
    )
    apply_crf_override()


def apply_crf_override():
    #-- Si VV_CRF está definido, parchea el escritor de vídeo de Manim para
    #-- codificar con ese CRF (calidad de máster). Si no, no toca nada.
    crf = os.environ.get("VV_CRF")
    if not crf:
        return

    def open_partial_movie_stream(self, file_path=None):
        if file_path is None:
            file_path = self.partial_movie_files[self.renderer.num_plays]
        self.partial_movie_file_path = file_path

        fps = scene_file_writer.to_av_frame_rate(config.frame_rate)
        codec = "libx264"
        pix_fmt = "yuv420p"
        options = {
                "an": "1",
                "crf": crf,
        }

        if config.movie_file_extension == ".webm":
            codec = "libvpx-vp9"
            options["-auto-alt-ref"] = "1"
            if config.transparent:
                pix_fmt = "yuva420p"
        elif config.transparent:
            codec = "qtrle"
            pix_fmt = "argb"

        video_container = scene_file_writer.av.open(
                file_path,
                mode="w",
        )
        stream = video_container.add_stream(
                codec,
                rate=fps,
                options=options,
        )
        stream.pix_fmt = pix_fmt
        stream.width = config.pixel_width
        stream.height = config.pixel_height

        self.video_container = video_container
        self.video_stream = stream
        self.queue = scene_file_writer.Queue()
        self.writer_thread = scene_file_writer.Thread(
                target=self.listen_and_write,
                args=(),
        )
        self.writer_thread.start()

    scene_file_writer.SceneFileWriter.open_partial_movie_stream = open_partial_movie_stream


# ----------------------------------------------------------------------------
# Escena base: pone la textura de papel detrás de todo
# ----------------------------------------------------------------------------
class InkScene(Scene):

    def setup(self):
        super().setup()
        self.camera.background_color = PAPER
        self.paper = None
        #-- La textura es opcional: sin paper_bg.png la escena sigue valiendo.
        if os.path.exists(PAPER_BG):
            bg = ImageMobject(PAPER_BG)
            bg.stretch_to_fit_width(config.frame_width)
            bg.stretch_to_fit_height(config.frame_height)
            bg.move_to(ORIGIN)
            bg.set_z_index(-100)
            self.add(bg)
            self.paper = bg


# ----------------------------------------------------------------------------
# Helpers mínimos de tinta
# ----------------------------------------------------------------------------
def M(*tex, color=INK, **kw):
    """MathTex con tinta por defecto."""
    return MathTex(*tex, color=color, **kw)


def accent(mob, *tex, color=OXBLOOD):
    """Colorea subcadenas de un MathTex con el acento. Devuelve el mob."""
    for t in tex:
        mob.set_color_by_tex(t, color)
    return mob


def ink_line(start, end, color=INK, stroke_width=5):
    """Trazo recto de tinta con extremos redondeados."""
    ln = Line(
            start,
            end,
            color=color,
            stroke_width=stroke_width,
    )
    ln.set_cap_style(CapStyleType.ROUND)
    return ln


def under_rule(mob, color=OXBLOOD, buff=0.14, sw=5):
    """La regla: subrayado fino en acento bajo un resultado. El cierre de la casa."""
    ln = Line(
            LEFT,
            RIGHT,
            color=color,
            stroke_width=sw,
    )
    ln.set_cap_style(CapStyleType.ROUND)
    ln.set_width(mob.width * 1.06)
    ln.next_to(
            mob,
            DOWN,
            buff=buff,
    )
    return ln


def soft_brace(mob, direction=DOWN, color=INK_SOFT):
    """Llave discreta para contar o agrupar sin gritar."""
    return Brace(
            mob,
            direction=direction,
            color=color,
    )
