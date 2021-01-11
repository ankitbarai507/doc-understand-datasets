import os
import random


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return random.randint(range_start, range_end)


from tempfile import NamedTemporaryFile

from InvoiceGenerator.api import Invoice, Item, Client, Provider, Creator
from InvoiceGenerator.pdf import SimpleInvoice
from pdf2image import convert_from_path, convert_from_bytes

# choose english as language
os.environ["INVOICE_LANG"] = "en"
num_invoices=100

for j in range(num_invoices):
	client = Client('Jio Platforms')
	provider = Provider('RIL', bank_account=str(random_with_N_digits(10)), bank_code=str(random_with_N_digits(6)))
	creator = Creator('Ankit Barai')

	invoice = Invoice(client, provider, creator)
	invoice.currency_locale = 'en_India.UTF-8'

	number_of_items=random.randint(5,20)

	for i in range(number_of_items):
		invoice.add_item(Item(random_with_N_digits(2), random_with_N_digits(3), description="Item "+str(i)))
		

	pdf = SimpleInvoice(invoice)
	pdf.gen('invoice/'+str(j)+".pdf")

	image_invoice = convert_from_bytes(open('invoice/'+str(j)+".pdf", 'rb').read(),single_file=True)
	image_invoice[0].save('invoice/'+str(j)+".png")
	os.remove('invoice/'+str(j)+".pdf") #delete the pdf now