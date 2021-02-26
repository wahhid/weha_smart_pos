#from escpos.printer import Usb
from xmlescpos.printer import Usb

# A wrapper to organise item names & prices into columns
class item:
    def __init__(self, name="", price="", dollarSign=False):
        self.name=name
        self.price=price
        self.dollarSign=dollarSign

    def encode(self):
        rightCols = 6
        leftCols = 24
        if(self.dollarSign):
            leftCols = leftCols / 2 - rightCols / 2
        left = self.name.ljust(int(leftCols))
        sign = "$" if self.dollarSign else ""
        right = (sign + self.price).rjust(int(rightCols))
        return (left + right + "\n").encode()

class Receipt01:

    def order_line_multiline(self, left_text,  right_text):
        x=15
        arr_left_text=[left_text[y-x:y] for y in range(x, len(left_text)+x,x)]
        multiline = ''
        first_row = True
        for text in arr_left_text:
            if first_row:
                first_row = False
                multiline += '<line>'
                multiline += '<left>' + text + '</left>'
                multiline += '<right>' + right_text + '</right>'
                multiline += '</line>'
            else:
                multiline += '<line>'
                multiline += '<left>' + text + '</left>'
                multiline += '<right></right>'
                multiline += '</line>'
        return multiline
                

    def print(self, pos_order, pos_order_lines):
        """ Seiko Epson Corp. Receipt Printer (EPSON TM-T88III) """
        p = Usb(0x0483, 0x5840, 0, 0x81, 0x03)
        #p = Usb(0x1504, 0x002a, 0, 0x81, 0x02)
        # with open("image.jpg", "rb") as image_file:
        #     data = base64.b64encode(image_file.read())

        receipt = ''
        receipt  += '<receipt>'        
        # receipt  += '<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQAQMAA..." />'
        receipt  += '<h1 align="center">WEHA Mart</h1>'
        receipt  += '<div align="center">Pondok Benda Timur 14B</div>'
        receipt  += '<div align="center">Pamulang, Tangerang Selatan</div>'
        receipt  += '<div align="center">NPWP: 12312412312312</div>'
        receipt  += '<br/>'
        receipt  += '<br/>'
        receipt  += '<line>'
        receipt  += '<left>Qty Item</left>'
        receipt  += '<right>Total</right>'
        receipt  += '</line>'
        receipt  += '<hr/>'
        for line in pos_order_lines:
            #multiline = self.order_line_multiline(line.name, str(line.price_subtotal_incl))
            #print(multiline)
            receipt += self.order_line_multiline(line.name, str(line.price_subtotal_incl))
            # receipt  += '<line>'
            # receipt  += '<left>' + line.name[0:24] + '</left>'
            # receipt  += '<right>' + str(line.price_subtotal_incl) + '</right>'
            # receipt  += '</line>'
        receipt  += '<hr/>'
        receipt  += '<line>'
        receipt  += '<left>Total</left>'
        receipt  += '<right>' + str(pos_order.amount_total) + '</right>'
        receipt  += '</line>'
        receipt  += '<br/>'
        receipt  += '<qr>31231231232193219312931293129</qr>'
        receipt  += '<barcode encoding="ean13" font="b">5449000000996</barcode>'
        receipt  += '</receipt>'
        
        p.receipt(receipt)
        # # Print top logo
        # p.set(align="center")
        # #logo_path = os.path.join(self.app_path, "ui/widget_product.ui")
        # #p.image("escpos-php.png", impl="bitImageColumn")

        # # Name of shop
        # p.set(align="center", width=2)
        # p.text("WEHA Mart.\n")
        # p.set(align="center")
        # p.text("Pamulang No. 42.\n")
        # p.text("\n")

        # # Title of receipt
        # p.set(align="center", text_type="B")
        # p.text("SALES RECEIPT\n")

        # # Items
        # p.set(align="left", text_type="B")
        # p.text(item(name="", price="$"))
        # p.set(align="left")
        # for line in pos_order_lines:
        #     print(line)
        #     print(line.name)
        #     print(line.price_subtotal_incl)
        #     it = item(name=line.name[0:24], price=str(line.price_subtotal_incl))
        #     p.text(it)
        #     #it = item(name="", price=str(line.price_subtotal_incl))
        #     #p.text(it)

        # self.subtotal = item(name="Subtotal", price=str(pos_order.amount_total))
        # p.set(text_type="B")
        # p.text(self.subtotal)
        # p.text("\n")

        # # Tax and total
        # self.tax = item(name="Tax", price=str(pos_order.amount_tax))
        # p.set()
        # p.text(self.tax)
        # p.set(width=2)
        # self.total = item(name="Total", price=str(pos_order.amount_total))
        # p.text(self.total)

        # # Footer
        # p.text("\n\n")
        # p.set(align="center")
        # p.text("Thank you for shopping at\nWEHA Mart.\n")
        # p.text("For trading hours, please visit weha-id.com\n")
        # p.text("\n\n")
        # p.text(self.date + "\n")
        # p.text("\n\n\n\n")
        # # Cut the paper
        # #p.cut()