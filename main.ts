import { readFileSync, writeFileSync, mkdirSync, statSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';

const source = resolve(process.env.MAKEFUN_BOT_DIR ?? '.', 'POST.json');
const destinationDir = resolve(process.env.MAKEFUN_OUTPUT_DIR ?? '/output');
const target = resolve(destinationDir, 'POST.json');

try {
  if (!existsSync(source)) {
    throw new Error(`Berkas sumber POST.json tidak ditemukan di ${source}`);
  }

  const contents = readFileSync(source);

  // Verifikasi format JSON valid sebelum menyalin
  JSON.parse(contents.toString('utf-8'));

  if (!existsSync(destinationDir)) {
    mkdirSync(destinationDir, { recursive: true });
  }

  writeFileSync(target, contents);

  const sourceSize = statSync(source).size;
  const targetSize = statSync(target).size;

  if (sourceSize !== targetSize) {
    throw new Error(`Ukuran berkas tidak cocok: sumber ${sourceSize} bytes vs target ${targetSize} bytes`);
  }

  console.log(`Copied and verified ${targetSize} bytes`);
} catch (failure) {
  const reason = failure instanceof Error ? failure.message : String(failure);
  console.error(`Gagal menyalin POST.json: ${reason}`);
  process.exitCode = 1;
}
