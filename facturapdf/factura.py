import calendar
import pdfkit
import jinja2
import math
import os
import locale
from random import randint as ran
from datetime import datetime

PDF_GENERATED = ''

def get_number():
    with open('facturapdf/Data/number.csv', 'rt') as n:
        return n.readline()


def set_number(number):
    with open('facturapdf/Data/number.csv', 'wt') as n:
        n.write(str(number))


def prepare_template(context):

    template_loader =  jinja2.FileSystemLoader('./')
    template_env = jinja2.Environment(loader=template_loader)

    html_template = 'facturapdf/Template/preview.html'
    template = template_env.get_template(html_template)
    output_text = template.render(context)

    return output_text


def create_pdf(**kwargs):

    # Variable validations
    receipt_number, month, year, pdf_name, context = validate_data(kwargs)

    # Prepare template
    template = prepare_template(context)

    # Prepare PDF
    css_style, config, output_pdf, final_folder, options = prepare_pdf(month, year, pdf_name)

    # Create PDF
    pdfkit.from_string(template, output_pdf, configuration=config, 
                    css=css_style, options=options)
    
    set_number(int(receipt_number) + 1)

    global PDF_GENERATED
    PDF_GENERATED = os.path.join(final_folder, pdf_name)
    print("Pdf generado: '{}'".format(PDF_GENERATED))
    # open_pdf()

def validate_data(kwargs):
    receipt_number = get_number()
    day = kwargs['date'][0:2]
    month = kwargs['date'][3:5]
    year = kwargs['date'][6:10]

    value = format_value(kwargs['value'])
    savings = format_value(kwargs['savings'])
    penalty = format_value(kwargs['penalty']) if kwargs['penalty'] > 0 else ""
    value_others = format_value(kwargs['value_others']) if kwargs['value_others'] > 0 else ""
    date_others = kwargs['date'] if value_others != "" else ""
    date_penalty = kwargs['date'] if penalty != "" else ""
    total = calcular_total(kwargs)

    desc_others = ': ' + kwargs['desc_others'] if not isinstance(kwargs['desc_others'], float) else ""

    pdf_name = '{}-{}-{}.pdf'.format(kwargs['apmt'], kwargs['name'], 
                                  kwargs['month_name'])

    context = {'day': day, 'month': month, 'year': year, 
               'receipt_number': receipt_number, 'name': kwargs['name'],
               'apmt': kwargs['apmt'], 'month_name': kwargs['month_name'],
               'type': kwargs['type'], 'value': value, 'date': kwargs['date'],
               'savings': savings, 'penalty': penalty, 'date_penalty': date_penalty,
               'total': total, 'value_others': value_others, 'date_others': date_others,
               'desc_others': desc_others}
               
    return receipt_number,month,year,pdf_name,context

def calcular_total(kwargs):
    total = kwargs['value'] + kwargs['savings']
    total = total + kwargs['penalty'] if kwargs['penalty'] > 0 else total
    total = total + kwargs['value_others'] if kwargs['value_others'] > 0 else total
    total = format_value(total)
    return total

def prepare_pdf(month, year, pdf_name):
    css_style = 'facturapdf/Template/style.css'
    wkhtmltopdf_path = 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
    
    english_month_name = calendar.month_name[int(month)]
    output_folder = 'facturapdf/Output/{}/{}-{}'.format(year, month, 
                                                english_month_name)
    output_pdf = output_folder + '/' + pdf_name
    
    final_folder = os.path.join(os.getcwd(), 
                                output_folder.replace('/', '\\'))
                 
    create_folder(final_folder)           

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
            'page-width': '118mm',
            'page-height': '120mm',
            'enable-local-file-access': None
        }
        
    return css_style,config,output_pdf,final_folder,options


def format_value(value):
    locale.setlocale(locale.LC_ALL, '')
    return locale.currency(value, grouping=True)


def create_folder(final_folder):
    if (not os.path.exists(final_folder)):
        try:
            folders = final_folder.split('\\')
            folder = '\\'.join(folders[:-1])
            
            os.mkdir(folder)
        except FileExistsError:
            pass
        finally:
            os.mkdir(final_folder)


def open_pdf():
    global PDF_GENERATED
    os.system('"{}"'.format(PDF_GENERATED))


if __name__ == '__main__':
    create_pdf()
