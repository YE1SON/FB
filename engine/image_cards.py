import os
import textwrap
from PIL import Image, ImageDraw, ImageFont, ImageOps

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FONT_CANDIDATES_BOLD = [
    os.path.join(BASE_DIR, "assets", "fonts", "Montserrat-Bold.ttf"),
    os.path.join(BASE_DIR, "assets", "fonts", "Roboto-Bold.ttf"),
    "/usr/share/fonts/truetype/roboto/unhinted/RobotoTTF/Roboto-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
    "C:/Windows/Fonts/calibrib.ttf",
    "C:/Windows/Fonts/segoeuib.ttf"
]

FONT_CANDIDATES_SERIF = [
    os.path.join(BASE_DIR, "assets", "fonts", "Merriweather-Regular.ttf"),
    os.path.join(BASE_DIR, "assets", "fonts", "Georgia.ttf"),
    "/usr/share/fonts/truetype/liberation2/LiberationSerif-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    "C:/Windows/Fonts/georgia.ttf",
    "C:/Windows/Fonts/times.ttf",
    "C:/Windows/Fonts/calibri.ttf"
]

def _get_font(preferred_path: str, fallback_list: list, size: int) -> ImageFont.ImageFont:
    if preferred_path and os.path.exists(preferred_path):
        try:
            return ImageFont.truetype(preferred_path, size)
        except Exception:
            pass
    for p in fallback_list:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    try:
        return ImageFont.load_default()
    except Exception:
        return None


def create_prayer_card_4_5(
    background_image_path: str,
    title: str,
    prayer_text: str,
    verse_footer: str,
    output_path: str,
    font_serif_path: str = "assets/fonts/Merriweather-Regular.ttf",
    font_bold_path: str = "assets/fonts/Montserrat-Bold.ttf"
) -> str:
    """
    Renderiza una Tarjeta de Oración vertical de alta fidelidad 1080x1350 (4:5 Feed de Facebook).
    - Aspect Ratio 4:5 exacto.
    - Overlay degradado oscuro para legibilidad garantizada.
    - Marco perimetral fino dorado (#D4AF37) con margen de 45px.
    - Tipografía sagrada jerárquica: Título dorado, cuerpo de oración cálido y versículo al pie.
    """
    WIDTH, HEIGHT = 1080, 1350
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    # 1. Cargar y ajustar imagen de fondo a 1080x1350
    if not os.path.exists(background_image_path):
        # Fallback a imagen de assets si la ruta es relativa
        alt_path = os.path.join(BASE_DIR, "assets", "images", os.path.basename(background_image_path))
        if os.path.exists(alt_path):
            background_image_path = alt_path
        else:
            # Crear fondo sobrio si no existe la imagen
            img_fallback = Image.new("RGBA", (WIDTH, HEIGHT), (20, 24, 33, 255))
            img_fallback.save(background_image_path, "JPEG")

    with Image.open(background_image_path).convert("RGBA") as base:
        bg = ImageOps.fit(base, (WIDTH, HEIGHT), method=Image.Resampling.LANCZOS)

        # 2. Crear overlay de gradiente oscuro para máxima legibilidad
        overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        draw_ov = ImageDraw.Draw(overlay)
        for y in range(HEIGHT):
            # Gradiente más oscuro hacia el centro e inferior
            alpha = int(90 + (y / HEIGHT) * 110)
            draw_ov.line([(0, y), (WIDTH, y)], fill=(12, 12, 16, min(alpha, 215)))

        combined = Image.alpha_composite(bg, overlay)

        # 3. Dibujar marco dorado interior
        draw = ImageDraw.Draw(combined)
        margin = 45
        gold_color = (212, 175, 55, 180)
        draw.rectangle(
            [(margin, margin), (WIDTH - margin, HEIGHT - margin)],
            outline=gold_color,
            width=2
        )

        # 4. Configurar fuentes con fallbacks seguros
        title_font = _get_font(font_bold_path, FONT_CANDIDATES_BOLD, 40)
        body_font = _get_font(font_serif_path, FONT_CANDIDATES_SERIF, 48)
        footer_font = _get_font(font_serif_path, FONT_CANDIDATES_SERIF, 32)

        # 5. Renderizar Título Superior
        title_text = title.strip().upper()
        t_bbox = draw.textbbox((0, 0), title_text, font=title_font)
        t_w = t_bbox[2] - t_bbox[0]
        draw.text(((WIDTH - t_w) / 2, 120), title_text, fill=(255, 215, 0, 255), font=title_font)

        # 6. Renderizar Cuerpo de la Oración (centrado con textwrap)
        lines = textwrap.wrap(prayer_text.strip(), width=32)
        line_height = 68
        total_text_height = len(lines) * line_height
        start_y = (HEIGHT - total_text_height) / 2 - 20

        for i, line in enumerate(lines):
            l_bbox = draw.textbbox((0, 0), line, font=body_font)
            l_w = l_bbox[2] - l_bbox[0]
            line_y = start_y + (i * line_height)

            # Drop shadow
            draw.text(((WIDTH - l_w) / 2 + 2, line_y + 2), line, fill=(0, 0, 0, 240), font=body_font)
            # Texto blanco cálido
            draw.text(((WIDTH - l_w) / 2, line_y), line, fill=(255, 253, 247, 255), font=body_font)

        # 7. Renderizar Pie / Versículo
        footer_text = verse_footer.strip() if verse_footer else "Whisper AMEN • Pass this covering to someone you love"
        f_bbox = draw.textbbox((0, 0), footer_text, font=footer_font)
        f_w = f_bbox[2] - f_bbox[0]
        footer_y = HEIGHT - 140
        draw.text(((WIDTH - f_w) / 2, footer_y), footer_text, fill=(220, 220, 225, 230), font=footer_font)

        # 8. Guardar resultado final
        final_rgb = combined.convert("RGB")
        final_rgb.save(output_path, "JPEG", quality=95)

    return output_path
