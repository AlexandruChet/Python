import qrcode

class QRGenerator:
    def __init__(self, data, filename="custom_qr.png"):
        self.data = data
        self.filename = filename

    def create_qr(self, fill_color="darkblue", back_color="white"):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(self.data)
        qr.make(fit=True)
        img = qr.make_image(fill_color=fill_color, back_color=back_color)
        img.save(self.filename)
        print(f"QR saved as {self.filename}")

link = input("Enter link: ")
qr = QRGenerator(link, "my_qr.png")
qr.create_qr()
