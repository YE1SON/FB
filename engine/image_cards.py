import os
import textwrap
from PIL import Image, ImageDraw, ImageFont, ImageOps

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FONT_CANDIDATES_TITLE = [
    os.path.join(BASE_DIR, "assets", "fonts", "Cinzel.ttf"),
    os.path.expanduser("~/.local/share/fonts/Cinzel.ttf"),
    "/home/ubuntu/.local/share/fonts/Cinzel.ttf",
    os.path.join(BASE_DIR, "assets", "fonts", "Montserrat-Bold.ttf"),
    "C:/Windows/Fonts/georgiab.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
    "/usr/share/fonts/truetype/liberation2/LiberationSerif-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
]

FONT_CANDIDATES_SERIF = [
    os.path.join(BASE_DIR, "assets", "fonts", "Cinzel.ttf"),
    os.path.expanduser("~/.local/share/fonts/Cinzel.ttf"),
    "/home/ubuntu/.local/share/fonts/Cinzel.ttf",
    os.path.join(BASE_DIR, "assets", "fonts", "Merriweather-Regular.ttf"),
    os.path.join(BASE_DIR, "assets", "fonts", "Georgia.ttf"),
    "C:/Windows/Fonts/georgia.ttf",
    "C:/Windows/Fonts/times.ttf",
    "/usr/share/fonts/truetype/liberation2/LiberationSerif-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
]

FONT_CANDIDATES_SANS = [
    os.path.join(BASE_DIR, "assets", "fonts", "Montserrat.ttf"),
    os.path.expanduser("~/.local/share/fonts/Montserrat.ttf"),
    "/home/ubuntu/.local/share/fonts/Montserrat.ttf",
    "C:/Windows/Fonts/arial.ttf",
    "C:/Windows/Fonts/calibri.ttf",
    "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
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
    watermark_text: str = "",
    font_serif_path: str = "",
    font_bold_path: str = ""
) -> str:
    """
    Renderiza una Tarjeta de Oración vertical de alta fidelidad 1080x1350 (4:5 Feed de Facebook).
    - Aspect Ratio 4:5 exacto.
    - Doble marco fino dorado (#D4AF37) con margen seguro de 45px y 55px.
    - Overlay degradado cinematográfico para legibilidad garantizada.
    - Título centrado en inglés con auto-ajuste de líneas.
    - Oración en tipografía noble con escalado dinámico inteligente para evitar recortes.
    - Versículo al pie con margen seguro.
    - Marca de agua sutil de la página de Facebook (@NombreDePagina).
    """
    WIDTH, HEIGHT = 1080, 1350
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    # 1. Cargar y ajustar imagen de fondo a 1080x1350
    if not os.path.exists(background_image_path):
        alt_path = os.path.join(BASE_DIR, "assets", "images", os.path.basename(background_image_path))
        if os.path.exists(alt_path):
            background_image_path = alt_path
        else:
            img_fallback = Image.new("RGBA", (WIDTH, HEIGHT), (18, 22, 30, 255))
            img_fallback.save(background_image_path, "JPEG")

    with Image.open(background_image_path).convert("RGBA") as base:
        bg = ImageOps.fit(base, (WIDTH, HEIGHT), method=Image.Resampling.LANCZOS)

        # 2. Overlay de gradiente oscuro cinematográfico
        overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        draw_ov = ImageDraw.Draw(overlay)
        for y in range(HEIGHT):
            # Degradado suave: más translúcido arriba (95) y más denso abajo (205) para máximo contraste
            alpha = int(90 + (y / HEIGHT) * 115)
            draw_ov.line([(0, y), (WIDTH, y)], fill=(10, 12, 16, min(alpha, 215)))

        combined = Image.alpha_composite(bg, overlay)
        draw = ImageDraw.Draw(combined)

        # 3. Dibujar Doble Marco Dorado de Alta Fidelidad
        gold_main = (212, 175, 55, 200)
        gold_sub = (212, 175, 55, 90)

        # Marco exterior (45px)
        margin_out = 45
        draw.rectangle(
            [(margin_out, margin_out), (WIDTH - margin_out, HEIGHT - margin_out)],
            outline=gold_main,
            width=2
        )
        # Marco interior fino (55px)
        margin_in = 55
        draw.rectangle(
            [(margin_in, margin_in), (WIDTH - margin_in, HEIGHT - margin_in)],
            outline=gold_sub,
            width=1
        )

        # Pequeños acentos en las 4 esquinas del marco
        corner_len = 16
        for cx, cy, dx, dy in [
            (margin_out, margin_out, 1, 1),
            (WIDTH - margin_out, margin_out, -1, 1),
            (margin_out, HEIGHT - margin_out, 1, -1),
            (WIDTH - margin_out, HEIGHT - margin_out, -1, -1)
        ]:
            draw.line([(cx, cy), (cx + dx * corner_len, cy)], fill=gold_main, width=3)
            draw.line([(cx, cy), (cx, cy + dy * corner_len)], fill=gold_main, width=3)

        # 4. Configurar fuentes
        title_font = _get_font(font_bold_path, FONT_CANDIDATES_TITLE, 36)
        footer_font = _get_font(font_serif_path, FONT_CANDIDATES_SERIF, 26)
        watermark_font = _get_font("", FONT_CANDIDATES_SANS, 21)

        # 5. Renderizar Título Superior (En Inglés, mayúsculas, centrado con auto-wrap)
        title_clean = title.strip().upper()
        title_lines = textwrap.wrap(title_clean, width=28)
        title_y = 100
        for t_line in title_lines:
            t_bbox = draw.textbbox((0, 0), t_line, font=title_font)
            t_w = t_bbox[2] - t_bbox[0]
            # Sombra suave
            draw.text(((WIDTH - t_w) / 2 + 1, title_y + 1), t_line, fill=(0, 0, 0, 220), font=title_font)
            # Texto dorado divino
            draw.text(((WIDTH - t_w) / 2, title_y), t_line, fill=(255, 215, 0, 255), font=title_font)
            title_y += 46

        # 6. Renderizar Marca de Agua Sutil (al pie inferior dentro del marco)
        has_watermark = bool(watermark_text and watermark_text.strip())
        if has_watermark:
            wm_text = watermark_text.strip()
            if not wm_text.startswith("@") and not wm_text.startswith("🕊️"):
                wm_text = f"🕊️ {wm_text}"
            wm_bbox = draw.textbbox((0, 0), wm_text, font=watermark_font)
            wm_w = wm_bbox[2] - wm_bbox[0]
            wm_y = HEIGHT - 100
            # Sutil dorado translúcido que protege la autoría sin estorbar
            draw.text(((WIDTH - wm_w) / 2, wm_y), wm_text, fill=(212, 175, 55, 140), font=watermark_font)

        # 7. Renderizar Pie / Versículo Bíblico (Sobre el pie inferior con margen seguro)
        footer_text = verse_footer.strip() if verse_footer else "Whisper AMEN • Pass this covering to someone you love"
        footer_lines = textwrap.wrap(footer_text, width=46)
        footer_base_y = (HEIGHT - 165) if has_watermark else (HEIGHT - 130)
        footer_start_y = footer_base_y - ((len(footer_lines) - 1) * 36)

        for fi, f_line in enumerate(footer_lines):
            f_bbox = draw.textbbox((0, 0), f_line, font=footer_font)
            f_w = f_bbox[2] - f_bbox[0]
            curr_fy = footer_start_y + (fi * 36)
            draw.text(((WIDTH - f_w) / 2 + 1, curr_fy + 1), f_line, fill=(0, 0, 0, 230), font=footer_font)
            draw.text(((WIDTH - f_w) / 2, curr_fy), f_line, fill=(225, 228, 235, 240), font=footer_font)

        # 8. Renderizar Cuerpo de la Oración (Cálculo Dinámico de Altura y Tamaño)
        # Espacio disponible vertical entre el título y el versículo
        content_top = title_y + 40
        content_bottom = footer_start_y - 40
        available_height = content_bottom - content_top

        # Escalamiento dinámico según longitud de la oración
        p_len = len(prayer_text.strip())
        if p_len <= 150:
            body_size = 44
            line_height = 68
            wrap_w = 30
        elif p_len <= 260:
            body_size = 38
            line_height = 58
            wrap_w = 34
        else:
            body_size = 32
            line_height = 48
            wrap_w = 40

        body_font = _get_font(font_serif_path, FONT_CANDIDATES_SERIF, body_size)
        body_lines = textwrap.wrap(prayer_text.strip(), width=wrap_w)
        total_body_h = len(body_lines) * line_height

        # Centrar exactamente en el área disponible
        start_y = content_top + max(0, (available_height - total_body_h) / 2)

        for i, line in enumerate(body_lines):
            l_bbox = draw.textbbox((0, 0), line, font=body_font)
            l_w = l_bbox[2] - l_bbox[0]
            line_y = start_y + (i * line_height)

            # Drop shadow negro para máxima legibilidad
            draw.text(((WIDTH - l_w) / 2 + 2, line_y + 2), line, fill=(0, 0, 0, 250), font=body_font)
            # Texto blanco perla cálido
            draw.text(((WIDTH - l_w) / 2, line_y), line, fill=(255, 253, 247, 255), font=body_font)

        # 9. Guardar resultado final
        final_rgb = combined.convert("RGB")
        final_rgb.save(output_path, "JPEG", quality=95)

    return output_path
