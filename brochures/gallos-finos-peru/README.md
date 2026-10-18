# Brochure para Gallos Finos Perú

Brochure comercial de Benigno Ranilla para este cliente. La fuente editable es `contenido.json` y el generador es `../../scripts/build_brochure.py` (requiere Python y ReportLab).

Ejecutar desde la raíz del repositorio: `python scripts/build_brochure.py`.

Salidas: página web en `docs/brochure-gallos-finos-peru.html`, plantilla Django equivalente, PDF en `output/pdf/` y copias descargables en ambos directorios static. La página está enlazada desde la sección Brochure del portafolio.

Referencias revisadas el 18 de octubre de 2026: https://gallosfinosperu.com/ y el portafolio de este repositorio. En la página de inicio del cliente se observaron enlaces a En vivo, Criadores, Programa, Admisión y Suscripciones; no se probaron sus procesos internos. Restaurantes y apuestas proceden del contexto proporcionado por el usuario. Los servicios son propuestas y no se atribuyen como implementaciones existentes.

Revisión comercial: el usuario confirma que desarrollamos la web y que contamos con sistemas de ventas, almacén, control de gastos y control documental. El brochure ampliado presenta seis áreas de solución, distingue sistemas disponibles de adaptaciones por validar y genera un PDF de cinco páginas, `benigno-ranilla-sistemas-gallos-finos-peru.pdf`.

Revisión 2: se eliminaron Entradas, socios y clientes y Personal y operación. Sistemas a medida pasa a ser el punto 06. PDF vigente guardado en `output/pdf/revision-2/`; los enlaces públicos conservan su ruta.
