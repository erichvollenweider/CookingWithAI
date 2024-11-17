from fpdf import FPDF
from flask import Blueprint, jsonify, session, make_response
from database.models import Recetas, Users

recetas_bp = Blueprint('recetas', __name__)

class CocinaPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.index = []
        self.add_page()

    def header(self):
        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(139, 69, 19)
        self.cell(0, 10, 'Recetario Personal', 0, 1, 'C')
        self.set_text_color(0, 0, 0)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 10)
        self.set_text_color(100)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

    def add_index(self):
        self.add_page()
        self.set_font('Helvetica', 'B', 16)
        self.set_fill_color(245, 245, 245)
        self.cell(0, 10, 'Índice', 0, 1, 'C', fill=True)
        self.ln(10)

        self.set_font('Helvetica', 'B', 14)
        self.set_fill_color(224, 224, 224)
        self.cell(160, 10, 'Título de la Receta', 1, 0, 'C', fill=True)
        self.cell(30, 10, 'Página', 1, 1, 'C', fill=True)

        self.set_font('Helvetica', '', 12)
        self.set_fill_color(245, 245, 245)
        for title, page in self.index:
            self.cell(160, 10, title, 1, 0, 'L', fill=True)
            self.cell(30, 10, str(page), 1, 1, 'C', fill=True)
        self.ln(10)

    def add_recipe(self, title, description):
        self.index.append((title, self.page_no()))

        self.set_font('Helvetica', 'B', 14)
        self.set_fill_color(255, 228, 196)
        self.cell(0, 10, title, 0, 1, 'L', fill=True)
        self.ln(5)

        sections = description.split('**')
        for section in sections:
            if section.startswith("Ingredientes:"):
                self.set_font('Helvetica', 'B', 12)
                self.set_text_color(160, 82, 45)
                self.cell(0, 10, 'Ingredientes:', 0, 1)
                self.set_font('Helvetica', '', 12)
                self.set_text_color(0, 0, 0)
                self.multi_cell(0, 8, section.replace("Ingredientes:", "").strip())
                self.ln(3)
            elif section.startswith("Preparación:"):
                self.set_font('Helvetica', 'B', 12)
                self.set_text_color(160, 82, 45)
                self.cell(0, 10, 'Preparación:', 0, 1)
                self.set_font('Helvetica', '', 12)
                self.set_text_color(0, 0, 0)
                self.multi_cell(0, 8, section.replace("Preparación:", "").strip())
                self.ln(3)
            elif section.startswith("Consejos:"):
                self.set_font('Helvetica', 'B', 12)
                self.set_text_color(160, 82, 45)
                self.cell(0, 10, 'Consejos:', 0, 1)
                self.set_font('Helvetica', '', 12)
                self.set_text_color(0, 0, 0)
                self.multi_cell(0, 8, section.replace("Consejos:", "").strip())
                self.ln(3)
            else:
                self.multi_cell(0, 8, section.strip())
        self.ln(10)

def sacar_titulo(description):
    start_ingredientes = description.find('**Ingredientes:**')

    if start_ingredientes == -1:
        return description

    return description[start_ingredientes:]

@recetas_bp.route('/export_recetas', methods=['GET'])
def export_recetas():
    if 'logged_in' not in session or not session['logged_in']:
        return jsonify({'message': 'Debes iniciar sesión'}), 401

    user_id = session['user_id']
    user = Users.query.get(user_id)

    if user is None:
        return jsonify({'message': 'Usuario no encontrado'}), 404

    recetas = Recetas.query.filter_by(user_id=user_id).all()

    if not recetas:
        return jsonify({'message': 'No tienes recetas para exportar'}), 404

    pdf = CocinaPDF()

    for receta in recetas:
        title = receta.titulo.strip().split('\n')[0]
        descripcion = sacar_titulo(receta.descripcion)
        pdf.add_recipe(title, descripcion)

    pdf.add_index()

    pdf_output = pdf.output(dest='S').encode('latin1')

    response = make_response(pdf_output)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=recetario_{user.username}.pdf'
    return response
