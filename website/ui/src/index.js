const m = require('mithril');

const Claim = require('./Claim.js');

m.route(document.body, '/', {
    '/': Claim
});
