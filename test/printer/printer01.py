from escpos.printer import Usb

""" Seiko Epson Corp. Receipt Printer (EPSON TM-T88III) """
p = Usb(0x0483, 0x5840, 0, 0x81, 0x03)
#p = Usb(0x5840, 0x0483, 0, 0x81, 0x03)

p.text("Hello World\n")
p.text("Hello World\n")
p.text("Hello World\n")
p.text("Hello World\n")
p.text("Hello World\n")
p.text("Hello World\n")
p.text("Hello World\n")
p.text("Hello World\n")

#p.image("logo.gif")
#p.barcode('1324354657687', 'EAN13', 64, 2, '', '')
#p.cut()
#p.close()