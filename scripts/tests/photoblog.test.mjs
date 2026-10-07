import assert from "node:assert/strict";
import test from "node:test";
import sharp from "sharp";
import { photoBytes } from "../../netlify/functions/photoblog.mjs";

for (const format of ["jpeg", "png", "webp"]) {
  test(`${format} uploads discard EXIF and XMP`, async () => {
    const original = await sharp({
      create: { width: 8, height: 5, channels: 3, background: "#fa6712" },
    }).toFormat(format).withExif({
      IFD0: { Artist: "Private photographer" },
      IFD3: { GPSLatitudeRef: "N", GPSLatitude: "47/1 22/1 0/1" },
    }).withXmp("<private>location metadata</private>").toBuffer();
    const input = await sharp(original).metadata();
    assert.ok(input.exif || input.xmp, "test input must contain private metadata");

    const result = await photoBytes(original.toString("base64"));
    assert.equal(result.extension, format === "jpeg" ? "jpg" : format);
    const output = await sharp(result.bytes).metadata();
    assert.equal(output.format, format);
    assert.equal(output.width, 8);
    assert.equal(output.height, 5);
    assert.equal(output.exif, undefined);
    assert.equal(output.xmp, undefined);
    assert.equal(output.iptc, undefined);
    assert.equal(output.icc, undefined);
  });
}

test("JPEG orientation is applied to pixels before EXIF is removed", async () => {
  const original = await sharp({
    create: { width: 8, height: 5, channels: 3, background: "#fa6712" },
  }).jpeg().withMetadata({ orientation: 6 }).toBuffer();
  const result = await photoBytes(original.toString("base64"));
  const output = await sharp(result.bytes).metadata();
  assert.equal(output.width, 5);
  assert.equal(output.height, 8);
  assert.equal(output.orientation, undefined);
  assert.equal(output.exif, undefined);
});

test("invalid image bytes are rejected before uploading", async () => {
  await assert.rejects(photoBytes(Buffer.from([0xff, 0xd8, 0xff, 0x00]).toString("base64")),
    /Could not process photo/);
});
