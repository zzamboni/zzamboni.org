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
    document: { querySelectorAll: selector => selector === '.article-content' ? [] : [gallery] },
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
      compareDocumentPosition(other) { return this.href < other.href ? 4 : 2; },
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
    document: { querySelectorAll: selector => selector === '.article-content' ? [] : galleries },
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

for (const mode of ['ordinary', 'picture', 'zoom-disabled', 'linked', 'nozoom', 'gallery', 'multiple']) {
  test(`standalone figure eligibility: ${mode}`, () => {
    let options, detached, wrapped;
    const img = {
      alt: 'Standalone', src: '/small.jpg', dataset: { zoomSrc: '/original.jpg' },
      closest: () => ['linked', 'nozoom'].includes(mode) ? {} : null,
      classList: { add(name) { assert.equal(name, 'nozoom'); } }
    };
    const parent = { insertBefore(link, media) { wrapped = media; } };
    const picture = { tagName: 'PICTURE', parentNode: parent };
    img.parentElement = mode === 'picture' ? picture : { tagName: 'FIGURE' };
    img.parentNode = parent;
    const caption = { textContent: 'Caption', innerHTML: '<em>Caption</em>' };
    const figure = {
      closest: () => mode === 'gallery' ? {} : null,
      querySelectorAll: () => mode === 'multiple' ? [img, img] : [img],
      querySelector: () => caption
    };
    const article = { querySelectorAll: () => [figure] };
    runInNewContext(source, {
      window: {
        matchMedia: () => ({ matches: false }),
        siteImageZoom: mode === 'zoom-disabled' ? undefined : { detach(image) { detached = image; } }
      },
      document: {
        querySelectorAll: selector => selector === '.article-content' ? [article] : [],
        createElement: () => ({
          appendChild() {}, addEventListener() {},
          querySelector: () => img, closest: () => figure
        })
      },
      GLightbox(config) { options = config; return { on() {} }; }
    });
    if (['ordinary', 'picture', 'zoom-disabled'].includes(mode)) {
      assert.equal(options.elements[0].href, '/original.jpg');
      assert.equal(options.elements[0].description, '<em>Caption</em>');
      assert.equal(wrapped, mode === 'picture' ? picture : img);
      assert.equal(detached, mode === 'zoom-disabled' ? undefined : img);
    } else {
      assert.equal(options, undefined);
      assert.equal(detached, undefined);
      assert.equal(wrapped, undefined);
    }
  });
}
