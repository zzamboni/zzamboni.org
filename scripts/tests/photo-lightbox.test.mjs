import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';
import { runInNewContext } from 'node:vm';

const source = readFileSync(new URL('../../assets/js/photo-lightbox.js', import.meta.url), 'utf8');

function slideOptions(caption) {
  let options;
  const link = {
    href: '/photo.jpg',
    querySelector: () => ({ alt: 'Accessible image description' }),
    closest: () => ({ querySelector: () => caption }),
    addEventListener() {}
  };
  const gallery = {
    classList: { contains: () => false },
    querySelectorAll: () => [link]
  };
  runInNewContext(source, {
    window: { matchMedia: () => ({ matches: false }) },
    document: { querySelectorAll: () => [gallery] },
    GLightbox(config) {
      options = config;
      return { on() {} };
    }
  });
  return options;
}

test('uses the rendered figure caption as the native slide description', () => {
  const options = slideOptions({
    textContent: 'Caption with a source',
    innerHTML: 'Caption with <em>a</em> <a href="/source/">source</a>'
  });
  assert.equal(options.elements[0].description,
    'Caption with <em>a</em> <a href="/source/">source</a>');
  assert.equal(options.elements[0].alt, 'Accessible image description');
  assert.equal(options.descPosition, 'bottom');
  assert.equal(options.moreLength, 0);
});

for (const [name, caption] of [
  ['absent', null],
  ['empty', { textContent: '', innerHTML: '' }],
  ['whitespace-only', { textContent: ' \n ', innerHTML: '<p> \n </p>' }]
]) {
  test(`${name} captions do not fall back to alt text`, () => {
    assert.equal(slideOptions(caption).elements[0].description, '');
  });
}

test('preserves encoded literal markup in captions', () => {
  const options = slideOptions({ textContent: '<example>', innerHTML: '&lt;example&gt;' });
  assert.equal(options.elements[0].description, '&lt;example&gt;');
});
