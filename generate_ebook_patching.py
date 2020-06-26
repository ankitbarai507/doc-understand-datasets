# from pdf2image import convert_from_path, convert_from_bytes

# image_invoices = convert_from_bytes(open('aho_ulman.pdf', 'rb').read())
# j=1
# for image in image_invoices:
#     image.save('invoice/'+str(j)+".png")
#     print(image.shape)
#     j+=1
#     if j>20:
#         break

#install PyMupdf
import fitz
import sys

pdffile = sys.argv[1]
low=int(sys.argv[2])
high=int(sys.argv[3])
op=sys.argv[4]
doc = fitz.open(pdffile)

for i in range(low,high):
    page = doc.loadPage(i) #number of page
    zoom = 4.5    # zoom factor
    mat = fitz.Matrix(zoom, zoom)
    pix = page.getPixmap(matrix = mat)
    output = op+str(i)+".png"
    pix.writePNG(output)