// Redirects legacy paper subdomains (iab.warondisease.org, wager.warondisease.org,
// impact.dih.earth, ...) to their canonical manual pages.
//
// The host map (redirect-map.json) and the route list (wrangler.jsonc) are both
// generated from _quarto-*.yml by scripts/generate_redirects.py. Do not add
// hosts here; add a dih-render.redirect-from field to the paper's config and
// regenerate.
import redirects from "./redirect-map.json";

const FALLBACK = "https://manual.warondisease.org/";

// Hosts that serve real content. The generated routes never match these, but
// if someone later adds a wildcard route in the dashboard, pass them through
// untouched instead of redirecting the live site.
const LIVE_HOSTS = new Set(["manual.warondisease.org"]);

export default {
  async fetch(request) {
    const url = new URL(request.url);
    const host = url.hostname.toLowerCase();

    if (LIVE_HOSTS.has(host)) {
      return fetch(request);
    }

    const target = redirects[host];
    const destination = target ? target + url.search : FALLBACK;
    return Response.redirect(destination, 301);
  },
};
