from pdf2image import convert_from_path, convert_from_bytes

image_invoices = convert_from_bytes(open('invoice/'+str(j)+".pdf", 'rb').read())
j=1
for image in image_invoices:
    image_invoice[0].save('invoice/'+str(j)+".png")
    j+=1
    if j>20:
        break