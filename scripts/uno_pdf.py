#!/usr/bin/env python3
"""Exporta un .docx a PDF con LibreOffice actualizando índices y campos (UNO).
Uso: python3 uno_pdf.py <entrada.docx> <salida.pdf>"""
import os, subprocess, sys, time, uno
from com.sun.star.beans import PropertyValue


def prop(n, v):
    p = PropertyValue(); p.Name = n; p.Value = v; return p


def main(src, dst):
    port = 2083
    proc = subprocess.Popen(["soffice", "--headless", "--invisible", "--nologo", "--norestore",
                             f"--accept=socket,host=127.0.0.1,port={port};urp;"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        local = uno.getComponentContext()
        resolver = local.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", local)
        for _ in range(60):
            try:
                ctx = resolver.resolve(f"uno:socket,host=127.0.0.1,port={port};urp;StarOffice.ComponentContext")
                break
            except Exception:
                time.sleep(1)
        desktop = ctx.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
        doc = desktop.loadComponentFromURL(uno.systemPathToFileUrl(os.path.abspath(src)), "_blank", 0,
                                           (prop("Hidden", True),))
        for _ in range(2):
            idx = doc.getDocumentIndexes()
            for i in range(idx.getCount()):
                idx.getByIndex(i).update()
            doc.getTextFields().refresh()
        doc.storeToURL(uno.systemPathToFileUrl(os.path.abspath(dst)), (prop("FilterName", "writer_pdf_Export"),))
        doc.close(True)
    finally:
        proc.terminate()


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
