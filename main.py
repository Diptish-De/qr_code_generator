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
from PIL import Image
import os


# ═══════════════════════════════════════════════════════════
#                    🎨 COLOR THEMES
# ═══════════════════════════════════════════════════════════

THEMES = {
    "1": {
        "name": "🟣 Neon Purple",
        "fill": (127, 0, 255),      # Purple
        "back": (0, 0, 0),          # Black
    },
    "2": {
        "name": "🔵 Ocean Blue",
        "fill": (0, 119, 182),      # Deep Blue
        "back": (255, 255, 255),    # White
    },
    "3": {
        "name": "🟠 Sunset",
        "fill": (255, 87, 51),      # Orange-Red
        "back": (25, 25, 25),       # Dark Gray
    },
    "4": {
        "name": "🟢 Matrix",
        "fill": (0, 255, 65),       # Bright Green
        "back": (0, 0, 0),          # Black
    },
    "5": {
        "name": "⚪ Classic",
        "fill": (0, 0, 0),          # Black
        "back": (255, 255, 255),    # White
    },
    "6": {
        "name": "💖 Pink Dream",
        "fill": (255, 20, 147),     # Deep Pink
        "back": (255, 240, 245),    # Lavender Blush
    },
    "7": {
        "name": "🌊 Gradient Ocean",
        "gradient": True,
        "center": (0, 191, 255),    # Deep Sky Blue
        "edge": (0, 0, 139),        # Dark Blue
        "back": (255, 255, 255),
    },
    "8": {
        "name": "🔥 Gradient Fire",
        "gradient": True,
        "center": (255, 215, 0),    # Gold
        "edge": (255, 0, 0),        # Red
        "back": (0, 0, 0),
    },
}

# ═══════════════════════════════════════════════════════════
#                    🔳 QR STYLES
# ═══════════════════════════════════════════════════════════

STYLES = {
    "1": {"name": "■ Square (Classic)", "drawer": SquareModuleDrawer()},
    "2": {"name": "● Rounded", "drawer": RoundedModuleDrawer()},
    "3": {"name": "○ Circle", "drawer": CircleModuleDrawer()},
    "4": {"name": "║ Vertical Bars", "drawer": VerticalBarsDrawer()},
    "5": {"name": "═ Horizontal Bars", "drawer": HorizontalBarsDrawer()},
    "6": {"name": "▢ Gapped Square", "drawer": GappedSquareModuleDrawer()},
}


def print_header():
    """Print a beautiful header."""
    print("\n")
    print("╔══════════════════════════════════════════════════════════╗")
    print("║           🔳  QR CODE GENERATOR  🔳                      ║")
    print("║                  by Diptish De                           ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()


def print_themes():
    """Display available themes."""
    print("┌──────────────────────────────────────┐")
    print("│         🎨 Available Themes          │")
    print("├──────────────────────────────────────┤")
    for key, theme in THEMES.items():
        print(f"│  [{key}] {theme['name']:<28} │")
    print("└──────────────────────────────────────┘")


def print_styles():
    """Display available QR styles."""
    print("┌──────────────────────────────────────┐")
    print("│          🔳 QR Code Styles           │")
    print("├──────────────────────────────────────┤")
    for key, style in STYLES.items():
        print(f"│  [{key}] {style['name']:<28} │")
    print("└──────────────────────────────────────┘")


def hex_to_rgb(hex_color: str) -> tuple:
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def generate_styled_qr(
    data: str,
    theme: dict,
    style_drawer,
    output_file: str = "qr_code.png",
    logo_path: str | None = None
):
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
        module_drawer=style_drawer,
        color_mask=color_mask,
    ).convert("RGBA")
    
    # Add logo if provided
    if logo_path and os.path.exists(logo_path):
        try:
            logo = Image.open(logo_path).convert("RGBA")
            qr_size = qr_img.size[0]
            logo_size = qr_size // 4
            
            # Create a white background circle for the logo
            logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
            
            pos = (
                (qr_size - logo_size) // 2,
                (qr_size - logo_size) // 2
            )
            
            # Create a white background behind logo
            bg = Image.new("RGBA", (logo_size + 20, logo_size + 20), (255, 255, 255, 255))
            bg_pos = (pos[0] - 10, pos[1] - 10)
            qr_img.paste(bg, bg_pos)
            qr_img.paste(logo, pos, logo)
            
            print(f"   ✓ Logo added successfully!")
        except Exception as e:
            print(f"   ⚠ Could not add logo: {e}")
    
    qr_img.save(output_file)
    return output_file


def get_custom_colors():
    """Get custom colors from user."""
    print("\n🎨 Enter custom colors (hex format, e.g., #FF5733):")
    
    fill_hex = input("   Foreground color: ").strip()
    if not fill_hex:
        fill_hex = "#000000"
    
    back_hex = input("   Background color: ").strip()
    if not back_hex:
        back_hex = "#FFFFFF"
    
    return {
        "name": "🎨 Custom",
        "fill": hex_to_rgb(fill_hex),
        "back": hex_to_rgb(back_hex),
    }


def main():
    """Main interactive function."""
    print_header()
    
    # Step 1: Get URL/Text
    print("📝 Step 1: Enter your data")
    print("─" * 40)
    data = input("   Enter URL or text: ").strip()
    
    if not data:
        print("\n❌ No input provided. Exiting.")
        return
    
    # Step 2: Choose theme
    print("\n🎨 Step 2: Choose a color theme")
    print("─" * 40)
    print_themes()
    print("   [C] 🎨 Custom Colors")
    theme_choice = input("\n   Select theme (1-8 or C): ").strip().upper()
    
    if theme_choice == "C":
        theme = get_custom_colors()
    else:
        theme = THEMES.get(theme_choice, THEMES["1"])
    
    print(f"   ✓ Selected: {theme['name']}")
    
    # Step 3: Choose style
    print("\n🔳 Step 3: Choose QR code style")
    print("─" * 40)
    print_styles()
    style_choice = input("\n   Select style (1-6): ").strip()
    style = STYLES.get(style_choice, STYLES["1"])
    print(f"   ✓ Selected: {style['name']}")
    
    # Step 4: Logo (optional)
    print("\n🖼️  Step 4: Add a logo (optional)")
    print("─" * 40)
    logo_path = input("   Enter logo path (or press Enter to skip): ").strip()
    if logo_path:
        logo_path = logo_path.strip('"').strip("'")
    else:
        logo_path = None
    
    # Step 5: Output filename
    print("\n💾 Step 5: Save your QR code")
    print("─" * 40)
    filename = input("   Filename (press Enter for 'qr_code.png'): ").strip()
    if not filename:
        filename = "qr_code.png"
    elif not filename.endswith(".png"):
        filename += ".png"
    
    # Generate QR Code
    print("\n" + "═" * 50)
    print("⚡ Generating your QR code...")
    print("═" * 50)
    
    output = generate_styled_qr(
        data=data,
        theme=theme,
        style_drawer=style["drawer"],
        output_file=filename,
        logo_path=logo_path,
    )
    
    print(f"\n✅ SUCCESS! QR code saved as: {output}")
    print(f"📂 Location: {os.path.abspath(output)}")
    print("\n" + "═" * 50)
    print("   Thank you for using QR Code Generator! 🎉")
    print("═" * 50 + "\n")


if __name__ == "__main__":
    main()
