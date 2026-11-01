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
    closest: () => null,
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

test('groups galleries by article, opens global indices and restores origin focus', () => {
  const article = {}, otherArticle = {};
  const instances = [];
  function gallery(scope, paths) {
    const links = paths.map(href => ({
      href,
      querySelector: () => ({ alt: href }),
      closest: () => ({ querySelector: () => null }),
      addEventListener(type, handler) { this[type] = handler; },
      focus(options) { this.focusOptions = options; }
    }));
    return {
      links,
      closest: () => scope,
      classList: { contains: () => false },
      querySelectorAll: () => links
    };
  }
  const galleries = [gallery(article, ['/a.jpg', '/b.jpg']),
    gallery(article, []), gallery(article, ['/c.jpg']),
    gallery(otherArticle, ['/d.jpg']), gallery(null, ['/e.jpg'])];
  runInNewContext(source, {
    window: { matchMedia: () => ({ matches: false }) },
    document: { querySelectorAll: () => galleries },
    GLightbox(config) {
      const instance = { config, events: {},
        on(name, handler) { this.events[name] = handler; },
        openAt(index) { this.index = index; }
      };
      instances.push(instance);
      return instance;
    }
  });
  assert.equal(instances.length, 3);
  assert.equal(instances[0].config.elements.map(e => e.href).join(','), '/a.jpg,/b.jpg,/c.jpg');
  const origin = galleries[2].links[0];
  let prevented = false;
  origin.click({ preventDefault() { prevented = true; } });
  assert(prevented);
  assert.equal(instances[0].index, 2);
  instances[0].events.close();
  assert.equal(origin.focusOptions.preventScroll, true);
  instances[0].index = null;
  origin.click({ ctrlKey: true, preventDefault() { assert.fail('Modified click intercepted'); } });
  assert.equal(instances[0].index, null);
});
