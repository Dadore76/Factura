import pandas
import factura as f

def generar_factura():
    data = leer_archivo()

    for record in data:
        f.create_pdf(date=record['date'],
                     name=record['name'],
                     apmt=record['apmt'],
                     value=record['value'],
                     type=record['type'],
                     month_name=record['month_name'],
                     savings=record['saving'],
                     penalty=record['penalty'],
                     desc_others=record['desc_others'],
                     value_others=record['value_others'],
                    )
        
def leer_archivo():
    df = pandas.read_csv('Data/generar.csv')
    return df.to_dict('records')

if __name__ == '__main__':
    generar_factura()
