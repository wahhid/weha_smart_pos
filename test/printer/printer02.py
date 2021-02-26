#from escpos.printer import Usb
from xmlescpos.printer import Usb

class Receipt01:

    def print(self):
        """ Seiko Epson Corp. Receipt Printer (EPSON TM-T88III) """
        p = Usb(0x0483, 0x5840, 0, 0x81, 0x03)

        p.receipt("""<receipt>
<h1 align="center">WEHA Mart</h1>
<div align="center">Pondok Benda Timur 14B</div>
<div align="center">Pamulang, Tangerang Selatan</div>
<div align="center">NPWP: 12312412312312</div>
<br/>
<br/>
<line>
<left>Qty Item</left>
<right>Total</right>
</line>
<hr/>
<line>
<left>1x Product</left>
<right>0.15</right>
</line>
<line>
<left>1x Product</left>
<right>0.15</right>
</line>
<line>
<left>1x Product</left>
<right>0.15</right>
</line>
<line>
<left>1x Product</left>
<right>0.15</right>
</line>
<line>
<left>1x Product</left>
<right>0.15</right>
</line>
<line>
<left>1x Product</left>
<right>34534543</right>
</line>



<hr/>
<line>
<left>Total</left>
<right>34534543.43</right>
</line>
<line>
<left>Paid</left>
<right>40000000</right>
</line>
<line>
<left>Change</left>
<right>2313123</right>
</line>
<br/>
<br/>
<div align="center">Terima Kasih</div>
</receipt>
                """)
        #p.receipt(data)
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

receipt01 = Receipt01()
receipt01.print()