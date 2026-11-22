// news-image-20261122 entry (Node 22, standard library only): the program
// validates the entry.png beside this file, then copies it to
// /output/entry.png (or $MAKEFUN_OUTPUT_DIR). The gate takes a whole PNG or
// JPEG of at most 1 MiB and 1024 by 1024 pixels, and the judge sees exactly
// the bytes copied. No network; deterministic: two runs write identical bytes.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { createHash } from 'node:crypto';
import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const ENTRY_SHA256 = '27151aae65b1723989a7e46d3af394632daac6791c4435bc9e754efb32de8142';
const MAX_BYTES = 1024 * 1024;
const MAX_DIM = 1024;
const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, 'entry.png');
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const dest = join(outDir, 'entry.png');

function fail(msg) {
  throw new Error(`entry check failed: ${msg}`);
}

if (!existsSync(source)) fail(`entry.png not found beside main.ts (${source})`);
const size = statSync(source).size;
if (size === 0) fail('entry.png is empty');
if (size > MAX_BYTES) fail(`entry.png is ${size} bytes, over the 1 MiB limit`);
const bytes = readFileSync(source);
if (!bytes.subarray(0, 8).equals(PNG_SIGNATURE)) {
  fail('entry.png does not start with the PNG signature');
}
// Dimensions from the IHDR chunk (bytes 16-23: width, height, big-endian).
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width === 0 || height === 0) fail('entry.png has a zero dimension');
if (width > MAX_DIM || height > MAX_DIM) {
  fail(`entry.png is ${width}x${height}, over the 1024x1024 limit`);
}
// The file must be a whole PNG: its last 12 bytes are the IEND chunk
// (4-byte length 0, "IEND", 4-byte CRC). A truncated file is refused.
const IEND = Buffer.from([0x00, 0x00, 0x00, 0x00, 0x49, 0x45, 0x4e, 0x44]);
if (size < 12 || !bytes.subarray(size - 12, size - 4).equals(IEND)) {
  fail('entry.png does not end with a complete IEND chunk');
}
const sha = createHash('sha256').update(bytes).digest('hex');
if (sha !== ENTRY_SHA256) fail(`entry.png sha256 mismatch: got ${sha}`);

mkdirSync(outDir, { recursive: true });
copyFileSync(source, dest);
const written = readFileSync(dest);
if (!written.equals(bytes)) fail('written entry.png does not match the source bytes');
console.log(`wrote ${dest}: ${written.length} bytes, sha256 ${sha}`);
