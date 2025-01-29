from flask import Flask, request, jsonify
from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont  # Dodane do obsługi czcionek TTF
import io
import json

app = Flask(__name__)

# Zarejestruj czcionkę DejaVuSans
pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))  # Upewnij się, że plik DejaVuSans.ttf jest w folderze

@app.route('/add_page', methods=['POST'])
def add_page():
    try:
        data = json.loads(request.data)

        numer_konta = data["Numer konta"]
        wartosc_netto = data["calkowitaWartoscNetto"]
        waluta = data["Waluta"]
        opis = data["opis"]

        # Tworzenie nowej strony PDF
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=A4)
        can.setFont("DejaVuSans", 12)  # Użyj zarejestrowanej czcionki
        can.drawString(50, 750, f"Numer konta: {numer_konta}")
        can.drawString(50, 730, f"Wartość netto: {wartosc_netto} {waluta}")
        can.drawString(50, 710, f"Opis: {opis}")
        can.save()

        packet.seek(0)
        new_page = PdfReader(packet).pages[0]

        # Sprawdź, czy plik istnieje
        try:
            existing_pdf = PdfReader("istniejacy_plik.pdf")
        except FileNotFoundError:
            return jsonify({"status": "error", "message": "Brak pliku istniejacy_plik.pdf"}), 400

        # Dodaj nową stronę
        output = PdfWriter()
        for page in existing_pdf.pages:
            output.add_page(page)
        output.add_page(new_page)

        # Zapisz zmiany
        with open("zmodyfikowany_plik.pdf", "wb") as output_pdf:
            output.write(output_pdf)

        return jsonify({"status": "success", "message": "Strona dodana pomyślnie!"})

    except Exception as e:
        print("Błąd:", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)