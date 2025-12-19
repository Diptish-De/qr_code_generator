#!/usr/bin/env python3
"""
Command-line QR Code Generator for GitHub Actions.
This script is designed to run non-interactively with command-line arguments.
"""

import argparse
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import (
    SquareModuleDrawer,
    RoundedModuleDrawer,
    CircleModuleDrawer,
    VerticalBarsDrawer,
    HorizontalBarsDrawer,
    GappedSquareModuleDrawer,
)
from qrcode.image.styles.colormasks import SolidFillColorMask, RadialGradiantColorMask


# ═══════════════════════════════════════════════════════════
#                    🎨 COLOR THEMES
# ═══════════════════════════════════════════════════════════

THEMES = {
    "1": {
        "name": "🟣 Neon Purple",
        "fill": (127, 0, 255),
        "back": (0, 0, 0),
    },
    "2": {
        "name": "🔵 Ocean Blue",
        "fill": (0, 119, 182),
        "back": (255, 255, 255),
    },
    "3": {
        "name": "🟠 Sunset",
        "fill": (255, 87, 51),
        "back": (25, 25, 25),
    },
    "4": {
        "name": "🟢 Matrix",
        "fill": (0, 255, 65),
        "back": (0, 0, 0),
    },
    "5": {
        "name": "⚪ Classic",
        "fill": (0, 0, 0),
        "back": (255, 255, 255),
    },
    "6": {
        "name": "💖 Pink Dream",
        "fill": (255, 20, 147),
        "back": (255, 240, 245),
    },
    "7": {
        "name": "🌊 Gradient Ocean",
        "gradient": True,
        "center": (0, 191, 255),
        "edge": (0, 0, 139),
        "back": (255, 255, 255),
    },
    "8": {
        "name": "🔥 Gradient Fire",
        "gradient": True,
        "center": (255, 215, 0),
        "edge": (255, 0, 0),
        "back": (0, 0, 0),
    },
}

# ═══════════════════════════════════════════════════════════
#                    🔳 QR STYLES
# ═══════════════════════════════════════════════════════════

STYLES = {
    "1": {"name": "■ Square (Classic)", "drawer": SquareModuleDrawer},
    "2": {"name": "● Rounded", "drawer": RoundedModuleDrawer},
    "3": {"name": "○ Circle", "drawer": CircleModuleDrawer},
    "4": {"name": "║ Vertical Bars", "drawer": VerticalBarsDrawer},
    "5": {"name": "═ Horizontal Bars", "drawer": HorizontalBarsDrawer},
    "6": {"name": "▢ Gapped Square", "drawer": GappedSquareModuleDrawer},
}


def generate_styled_qr(data: str, theme: dict, style_drawer, output_file: str):
    """Generate a beautifully styled QR code."""
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=12,
        border=4,
    )
    
    qr.add_data(data)
    qr.make(fit=True)
    
    # Create color mask based on theme
    if theme.get("gradient"):
        color_mask = RadialGradiantColorMask(
            back_color=theme["back"],
            center_color=theme["center"],
            edge_color=theme["edge"],
        )
    else:
        color_mask = SolidFillColorMask(
            back_color=theme["back"],
            front_color=theme["fill"],
        )
    
    # Generate styled QR image
    qr_img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=style_drawer(),
        color_mask=color_mask,
    ).convert("RGBA")
    
    qr_img.save(output_file)
    return output_file


def parse_choice(choice_str: str) -> str:
    """Extract the number from choice string like '1 - Square'."""
    return choice_str.split(" ")[0].strip()


def main():
    parser = argparse.ArgumentParser(
        description="🔳 QR Code Generator - CLI Version",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    parser.add_argument(
        "--data", "-d",
        required=True,
        help="URL or text to encode in the QR code"
    )
    
    parser.add_argument(
        "--theme", "-t",
        default="5",
        help="Color theme (1-8)"
    )
    
    parser.add_argument(
        "--style", "-s",
        default="1",
        help="QR code style (1-6)"
    )
    
    parser.add_argument(
        "--output", "-o",
        default="qr_code.png",
        help="Output filename"
    )
    
    args = parser.parse_args()
    
    # Parse theme and style choices
    theme_key = parse_choice(args.theme)
    style_key = parse_choice(args.style)
    
    theme = THEMES.get(theme_key, THEMES["5"])
    style = STYLES.get(style_key, STYLES["1"])
    
    print("═" * 50)
    print("🔳 QR Code Generator - GitHub Actions")
    print("═" * 50)
    print(f"📝 Data: {args.data}")
    print(f"🎨 Theme: {theme['name']}")
    print(f"🔲 Style: {style['name']}")
    print(f"💾 Output: {args.output}")
    print("═" * 50)
    
    output = generate_styled_qr(
        data=args.data,
        theme=theme,
        style_drawer=style["drawer"],
        output_file=args.output,
    )
    
    print(f"\n✅ SUCCESS! QR code saved as: {output}")
    print("═" * 50)


if __name__ == "__main__":
    main()
