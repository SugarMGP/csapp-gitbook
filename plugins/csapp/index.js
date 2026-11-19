const { load } = require('cheerio');
const highlight = require('highlight.js');
let documents = {};

module.exports = {
  hooks: {
    init() {
      documents = {};
      highlight.registerAliases('asm', { languageName: 'x86asm' });
      // CSAPP's hardware control language has no bundled highlighter.
      highlight.registerAliases('hcl', { languageName: 'plaintext' });
    },
    page(page) {
      if (this.output.name !== 'website') return page;
      const $ = load(page.content, null, false);
      const headings = $('h1,h2,h3,h4,h5,h6');
      const offset = headings.length ? 1 - Number(headings[0].name[1]) : 0;
      headings.each((_, heading) => {
        heading.name = 'h' + Math.min(6, Math.max(1, Number(heading.name[1]) + offset));
      });
      page.content = $.html();
      if (page.path.endsWith('/chapter.md')) {
        const counts = new Map();
        // Match the upstream generator's Unicode slugs, including repeated headings.
        $('h1,h2,h3,h4,h5,h6').each((_, heading) => {
          const base = $(heading).text().replace(/[`*_~]/g, '').trim().toLowerCase()
            .replace(/[^\p{L}\p{N}_ -]/gu, '').replace(/ /g, '-');
          const count = counts.get(base) || 0;
          counts.set(base, count + 1);
          $(heading).attr('id', count ? `${base}-${count}` : base);
        });
        page.content = $.html();
      }
      if (page.search !== false && !/(^|\/)(README|UPSTREAM)\.md$/.test(page.path)) {
        $('p,li,tr,pre,h1,h2,h3,h4,h5,h6,blockquote').append(' ');
        const body = $.root().text().replace(/\s+/g, ' ').trim()
          .replace(/[&<>]/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[char]));
        const url = this.output.toURL(page.path);
        documents[url] = { url, title: page.title, body, keywords: '' };
      }
      return page;
    },
    finish() {
      if (this.output.name === 'website') {
        return this.output.writeFile('search_plus_index.json', JSON.stringify(documents));
      }
    }
  }
};
