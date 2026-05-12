from flask import Flask, render_template, request, send_file, abort
import requests
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from io import BytesIO
import os

app = Flask(__name__)
BACKEND_URL = os.getenv('BACKEND_URL', 'http://backend:8000')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generar-pdf', methods=['POST'])
def generar_pdf():
    try:
        id_factura = request.form['id_factura']
        response = requests.get(f'{BACKEND_URL}/facturas/v1/{id_factura}')
        if response.status_code != 200:
            abort(404, description="Factura no encontrada")
        factura = response.json()

        # Crear buffer y doc para la creación del PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4,
                                rightMargin=20*mm, leftMargin=20*mm,
                                topMargin=20*mm, bottomMargin=20*mm)
        styles = getSampleStyleSheet()
        elements = []

        # Título e ID
        elements.append(Paragraph("FACTURA", styles['Title']))
        elements.append(Paragraph(f"Número: {factura['numero_factura']}", styles['Normal']))
        elements.append(Paragraph(f"Fecha: {factura['fecha_emision']}", styles['Normal']))
        elements.append(Spacer(1, 10*mm))

        # Información de la Empresa
        elements.append(Paragraph("EMPRESA", styles['Heading2']))
        empresa = factura['empresa']
        elements.append(Paragraph(f"Nombre: {empresa['nombre']}", styles['Normal']))
        elements.append(Paragraph(f"Dirección: {empresa['direccion']}", styles['Normal']))
        elements.append(Paragraph(f"Teléfono: {empresa['telefono']}", styles['Normal']))
        elements.append(Paragraph(f"Email: {empresa['email']}", styles['Normal']))
        elements.append(Spacer(1, 8*mm))

        # Información del Cliente
        elements.append(Paragraph("CLIENTE", styles['Heading2']))
        cliente = factura['cliente']
        elements.append(Paragraph(f"Nombre: {cliente['nombre']}", styles['Normal']))
        elements.append(Paragraph(f"Dirección: {cliente['direccion']}", styles['Normal']))
        elements.append(Paragraph(f"Teléfono: {cliente['telefono']}", styles['Normal']))
        elements.append(Spacer(1, 8*mm))

        # Detalle de la Factura
        elements.append(Paragraph("DETALLE", styles['Heading2']))
        tabla_data = [['Descripción', 'Cantidad', 'Precio Unitario', 'Total']]
        for item in factura['detalle']:
            tabla_data.append([
                item['descripcion'],
                str(item['cantidad']),
                f"${item['precio_unitario']:.2f}",
                f"${item['total']:.2f}"
            ])
        tabla = Table(tabla_data, colWidths=[90*mm, 25*mm, 35*mm, 25*mm])
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ]))
        elements.append(tabla)
        elements.append(Spacer(1, 8*mm))

        # Subtotal, Impuesto y Total
        resumen_data = [
            ['Subtotal:', f"${factura['subtotal']:.2f}"],
            ['Impuesto (21%):', f"${factura['impuesto']:.2f}"],
            ['TOTAL:', f"${factura['total']:.2f}"],
        ]
        resumen = Table(resumen_data, colWidths=[130*mm, 45*mm])
        resumen.setStyle(TableStyle([
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 2), (-1, 2), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 2), (-1, 2), 12),
            ('LINEABOVE', (0, 2), (-1, 2), 1, colors.black),
        ]))
        elements.append(resumen)

        # Generar el doc y limpiar el buffer
        doc.build(elements)
        buffer.seek(0)

        # Retornar el PDF para visualizar y descargar
        return send_file(
            buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"factura_{id_factura}.pdf"
        )

    except requests.exceptions.ConnectionError:
        abort(503, description="Error de conexión con el servidor")
    except Exception as e:
        abort(500, description=str(e))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)