const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const attrs = {'aria-pressed':'false'};
const label = {textContent:'Pause motion'};
let click;
let paused;
const images = [{src:'https://example.com/website/assets/fleet-orbit.svg'}];
const control = {
  addEventListener: (event, handler) => { assert.equal(event, 'click'); click = handler; },
  getAttribute: key => attrs[key],
  setAttribute: (key,value) => { attrs[key] = value; },
  querySelector: () => label,
};
const document = {
  documentElement: {classList: {add(){}, toggle(name,value){paused=value;}}},
  addEventListener(){},
  querySelector: selector => selector === '.motion-toggle' ? control : null,
  querySelectorAll: selector => selector === 'img[src*=".svg"]' ? images : [],
};
vm.runInNewContext(fs.readFileSync('assets/site.js','utf8'), {document,URL});
click();
assert.equal(attrs['aria-pressed'],'true');
assert.equal(attrs['aria-label'],'Resume illustration animations');
assert.equal(label.textContent,'Resume motion');
assert.equal(images[0].src,'https://example.com/website/assets/fleet-orbit.svg#still');
assert.equal(paused,true);
click();
assert.equal(attrs['aria-pressed'],'false');
assert.equal(images[0].src,'https://example.com/website/assets/fleet-orbit.svg');
assert.equal(paused,false);
console.log('Motion toggle: pause and resume pass.');
