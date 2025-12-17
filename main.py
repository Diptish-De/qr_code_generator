import qrcode
from PIL import Image


def generate_qr(
    data: str,
    fill_color: str = "black",
    back_color: str = "white",
    output_file: str = "qr_code.png",
    logo_path: str | None = None
):
    """
    Generate a styled QR code.

    :param data: Text or URL for the QR code
    :param fill_color: QR foreground color
    :param back_color: QR background color
    :param output_file: Output image filename
    :param logo_path: Optional logo image path
    """

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=12,
        border=4,
    )

    qr.add_data(data)
    qr.make(fit=True)

    qr_img = qr.make_image(
        fill_color=fill_color,
        back_color=back_color
    ).convert("RGBA")

    # Add logo if provided
    if logo_path:
        logo = Image.open(logo_path).convert("RGBA")

        qr_size = qr_img.size[0]
        logo_size = qr_size // 4
        logo = logo.resize((logo_size, logo_size))

        pos = (
            (qr_size - logo_size) // 2,
            (qr_size - logo_size) // 2
        )

        qr_img.paste(logo, pos, logo)

    qr_img.save(output_file)
    print(f"✅ QR code saved as {output_file}")


if __name__ == "__main__":
    print("🔳 QR Code Generator")
    print("-" * 30)
    
    # Get URL from user
    url = input("Enter the URL or text for QR code: ").strip()
    
    if not url:
        print("❌ No input provided. Exiting.")
    else:
        # Optional: Ask for custom filename
        filename = input("Enter filename (press Enter for 'qr_code.png'): ").strip()
        if not filename:
            filename = "qr_code.png"
        elif not filename.endswith(".png"):
            filename += ".png"
        
        generate_qr(
            data=url,
            fill_color="#7F00FF",
            back_color="#000000",
            output_file=filename,
            logo_path=None
        )
