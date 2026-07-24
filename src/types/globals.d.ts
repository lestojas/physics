// Type declaration for pdf-parse's internal module path.
// We import "pdf-parse/lib/pdf-parse.js" directly to avoid the package's
// top-level "debug mode" that reads a bundled test PDF. That deep path is not
// covered by @types/pdf-parse, so we declare a minimal shape here.
declare module "pdf-parse/lib/pdf-parse.js" {
  interface PdfParseResult {
    text: string;
    numpages: number;
    info: unknown;
  }
  function pdfParse(dataBuffer: Buffer): Promise<PdfParseResult>;
  export default pdfParse;
}
