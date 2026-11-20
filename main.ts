import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { resolve } from 'node:path';

const source = resolve(process.env.MAKEFUN_BOT_DIR ?? '/bot', 'POST.json');
const destination = resolve(process.env.MAKEFUN_OUTPUT_DIR ?? '/output');

try {
  const contents = readFileSync(source);
  mkdirSync(destination, { recursive: true });
  writeFileSync(resolve(destination, 'POST.json'), contents);
} catch (failure) {
  const reason = failure instanceof Error ? failure.message : String(failure);
  console.error(`Gagal menyalin POST.json: ${reason}`);
  process.exitCode = 1;
}
