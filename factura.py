import pdfkit
import jinja2
import os
from random import randint as ran
from datetime import datetime

PDF_GENERATED = ""

def validate_data(**kwargs):
    pass

def prepare_template(context):

    # validations = validate_data(context)

    # if validations:
    #     raise ValueError (validations)

    template_loader =  jinja2.FileSystemLoader("./")
    template_env = jinja2.Environment(loader=template_loader)

    html_template = "Template/preview.html"
    template = template_env.get_template(html_template)
    output_text = template.render(context)

    return output_text

def create_pdf():

    # Variable validations
    day = f"{datetime.today().day:02}"
    month = f"{datetime.today().month:02}"
    year = str(datetime.today().year)
    receipt_number = ran(1000, 10000)
    name = "Juan"
    apmt = "502"
    month_name = "Julio"

    context = {'day': day, 'month': month, 'year': year, 
            'receipt_number': receipt_number, 'name': name,
            'apmt': apmt, 'month_name': month_name}

    # Prepare template
    template = prepare_template(context)

    # Prepare PDF
    css_style = "Template/style.css"
    wkhtmltopdf_path = "C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
    output_pdf = "Output/pdfGenerado.pdf"

    options = {
            # 'page-size' : 'B7',
            # 'orientation' : 'Landscape',
            # 'encoding' : 'UTF-8',
            # 'print_media_type' : False,
            # 'title' : context_dict.get('RECIBO DE PAGO', 'PDF'),
            'margin-top' : '4mm',
            'margin-bottom' : '0mm',
            'margin-left' : '3mm',
            'margin-right' : '0mm',
            'page-width': '113mm',
            'page-height': '115mm',
            'enable-local-file-access': None
        }

    # Create PDF
    pdfkit.from_string(template, output_pdf, configuration=config, 
                    css=css_style, options=options)
    
    full_path = os.getcwd()
    global PDF_GENERATED
    PDF_GENERATED = os.path.join(full_path, output_pdf)

def open_pdf():
    global PDF_GENERATED
    os.system(PDF_GENERATED)
    # print(PDF_GENERATED)


if __name__ == "__main__":
    create_pdf()
