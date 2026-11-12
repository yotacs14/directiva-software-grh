#!/usr/bin/env python3
"""Exporta un .docx a PDF con LibreOffice actualizando índices y campos (UNO).
Uso: python3 uno_pdf.py <entrada.docx> <salida.pdf> [--docx-actualizado <salida.docx>]
--docx-actualizado: guarda además el .docx con el índice de contenido ya calculado
(Word muestra el índice sin necesidad de actualizar campos)."""
import os, subprocess, sys, time, uno
from com.sun.star.beans import PropertyValue


def prop(n, v):
    p = PropertyValue(); p.Name = n; p.Value = v; return p


def main(src, dst, docx_out=None):
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
        if docx_out:
            doc.storeToURL(uno.systemPathToFileUrl(os.path.abspath(docx_out)), (prop("FilterName", "MS Word 2007 XML"),))
        doc.close(True)
    finally:
        proc.terminate()


if __name__ == "__main__":
    a = sys.argv[1:]
    main(a[0], a[1], a[a.index("--docx-actualizado") + 1] if "--docx-actualizado" in a else None)
