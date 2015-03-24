---

# Client-Side Unit Testing with Zuul and Tape

### Amadeus Junqueira

twitter: [@_4m4deus](https://twitter.com/_4m4deus)

blarg: [www.rippityrippity.me](http://rippityrippity.me/)

---

### Most examples use Browserify, the node-like module system for the browser

If you've worked with node you should be familiar with it
```js
// hey.js
module.exports = function hey() {
  return 'heyyyyyyyyyyy';
}

// ya.js
module.exports = function ya() {
  return 'yaaaaaaaaaa!';
};

// mega-hit.js
var lyric1 = require('./hey');
var lyric2 = require('./ya');

function multiNationalMegaHit() {
  return lyric1() + ' ' + lyric2();
};

console.log(multiNationalMegaHit());
// heyyyyyyyyyyy yaaaaaaaaaa!
```

---
class: middle, center

# Obligatory _Why unit tests?_

### &lsquo;Caffeine & intuition only carry you so far&rsquo; &ndash; Ben Alman

<p class="img-cont">
<img src="http://media4.giphy.com/media/lCeASPqq2UN8I/200.gif" />
</p>

---

### - Your code will (likely) improve
### - Regression testing, does my change break shit?
### - Do different browsers behave differently?  (hint: _Duh!_)

&nbsp;
&nbsp;
&nbsp;
&nbsp;
<p class="img-cont">
<img src="http://media1.giphy.com/media/VDZFZRTmzt7cQ/200.gif" />
</p>

---

### - Discover the presence of a previously unknown bug
&nbsp;
&nbsp;
&nbsp;
&nbsp;
<p class="img-cont">
<img width="500" src="http://media2.giphy.com/media/8va99bCj63Kus/200.gif" />
</p>

---
class: middle, center
# Need a framework?
<p class="img-cont">
<img width="500" src="http://media4.giphy.com/media/ibOEGsIGd3jtS/200.gif" />
</p>
---
# Tape by substack

A tap-producing test harness for node and browsers. TAP (test anything protocol) is a standard for test output.

###- TAP allows for the dead simple integration of many consumers
###- Keeps testing simple

<p class="img-cont">
<img src="http://substack.net/images/substack.png" />
</p>

---
### Keep it simple, stupid

Why do I need `it`, `describe`, `beforeEach`, `afterEach` adding to my cognitive load!?

Mocha

```js
var assert = require("assert")


describe('truth', function(){
  beforeEach(function(){ // set something up })
  it('should find the truth', function(){
    assert.equal(1, 1);
  })
  afterEach({ // tear something down })
})
```
Tape

```js
var test = require('tape');

test('equivalence', function(t) {
  t.ok(1 === 1, 'these two numbers are equal');
  t.end();
});

```
---

## Testing async code with Tape

All you _really_ need is `t.plan` or `t.end`

```js
var asyncModule = require('../lib/module');

test('async1', function(t) {
  asyncModule(function(){
    t.ok(true, 'callback was called!');
    t.end();
  })
});

test('async1', function(t) {
  t.plan(1);
  asyncModule(function(){
    t.ok(true, 'callback was called!');
  })
});

```
---

### Advantages of Tape:

1. It’s easier to understand
2. The tests are _just_ code: you can often run tests with `node test/test.js`
3. No need for some `test runner` binary that contains some of the code the test really needs
4. Powerful ecosystem of TAP test consumers
---

class: middle, center

# Making your code testable in javascript!

### Basic advice from a former testing-n00b

---
class: center, middle

## Mock your ajax tests

It's often a good idea to pass in external dependencies

---
Mock your ajax tests

```js
// Don't
var xhr = require('xhr');

module.exports = function myModule() {
  xhr('/route', function(err){ ... });
};

// Do
var ok = require('assert').ok

module.exports = function myModule(xhr) {
  ok(!!xhr, 'required: xhr');
  xhr('/route', function(err, results){
    return results;
  });
};

// some-test.js
var test = require('tape');
var module = require('./my-module');

test('request completes', function(t){
  module(mockXhr);
  function mockXhr(route, cb){
    t.ok('done' === cb('done'), 'should return results');
    t.end();
  }
})

```
---

## Throw your own errors

aka catch programmer errors!  Your unit tests should cover this.


```js
var ok = require('assert').ok

module.exports = function someModule(opts) {
  ok(!!opts, 'required: opts');
  ok(!!opts.dao, 'required: .dao');
  ok(!!opts.cb, 'required: .cb');

  opts.dao.get({ specific: 'data' }, opts.cb);
}
```

---
class: center, middle
## Event handling

####- Move application logic from event handlers
####- Don't pass the event object around!
---

```js
module.exports = MyApp = {
  handleClick: function(event) {
    this.showPopup(event.clientX, event.clientY);
  },
  showPopup: function(x, y) {
    var popup = document.getElementById('popup');
    popup.style.left = x + 'px';
    popup.style.top = y + 'px';
    popup.className = 'reveal';
  }
};

addListener(element, 'click', function(event) {
  MyApp.handleClick(event); // this is okay
});
```
```js
// test.js
var app = require('./app')
var test = require('tape');
var popup = document.createElemnt('div');
popup.id = 'popup';
document.body.appendChild(popup);

test('show popup should add correct styles',function() {
  app.showPopup(12, 24);
  t.ok(popup.style.left === 12, 'left');
  t.ok(popup.style.top === 24, 'top');
  t.ok(popup.classList.contains('reveal'), 'classname');
});
```

###### Extended from `Maintainable Javascript` by Zakas
---

### Testing Events with dom-events

```js
function component() {
  var el = document.createElement('a');
  a.href = '#';
  el.classList.add('active');
  addListener(el, 'click', function(e){
    e.preventDefault();
    toggle()
  })
  function toggle() { el.classList.toggle('active') }
  return el;
}

var test = require('tape');
var dom = require('dom-events');

test('component should toggle class when clicked', function(t){
  t.plan(1);
  var el = component();
  dom.emit(el, 'click')
  ok(!ok.classList.contains('active'), 'no active class after click');
})
```
---
class: center, middle

# Keep it functional!

Input, output, test, repeat.

---
Keep it functional!
```js
// Don't.
module.exports = {
  lyric: 'hey',
  getLyric: function getLyric() {
    return this.thaHook();
  },
  thaHook: function thaHook() {
    return this.lyric + ' ya!';
  }
}

//Do
module.exports = {
  lyric: 'hey',
  getLyric: function getLyric() {
    return this.thaHook(this.lyric);
  },
  thaHook: function thaHook(lyric) {
    return lyric + ' ya!';
  }
}

// test.js
var lyric = require('./lyric');
var test = require('tape');
test('tha hook should be a multinational megahit', function(t) {
  t.ok(lyric.thaHook('hell') === 'hell ya!', 'still probably a hit');
})

```
---
# Testability with module systems

<p class="img-cont">
<img style="width:100%" src='https://www.evernote.com/shard/s471/sh/6d64ac7f-f7f8-4390-bcf7-8736c0e02b46/c2525649460de075ec2e15a45f0c38c9/deep/0/Derick-Bailey-on-Twitter--"-autodoc--"Hey,-this-function-is-private-but-I-want-to-test-it-anyway."-...--sigh-NO".png' />
</p>

---

# A private function of great responsibility

```js
module.exports = React.createClass({
  render: function render() {
    var list = getFilteredList(this.props.lists, this.state);

    return (
      <div>{list}</div>
    );
  }

})

// SHIT this is reeeallly important I want to test it!

function getFilteredList(lists, state) {
  var neither = !state.filterOne && !state.filterTwo;
  if (neither) return lists.one.map(mapFn).concat(lists.two.map(mapFn));
  else if (state.filterOne) return lists.one.map(mapFn);
  else if (state.filterTwo) return lists.two.map(mapFn);
  return [];
}

function mapFn(obj){ return obj.name; }

```

---

### If a private method's logic is complex and important, move it to it's own module and test it


Don't: expose private functions just to test them!

```js

module.exports = React.createClass({...})

module.exports._private = {
  getFilteredList: getFilteredList
};

```

Do: create a new module!

```bash
$ touch get-filtered-list.js
$ vi get-filtered-list.js
```

```js
module.exports = function getFilteredList(lists, state) {
  var neither = !state.filterOne && !state.filterTwo;
  if (neither) return lists.one.map(mapFn).concat(lists.two.map(mapFn));
  else if (state.filterOne) return lists.one.map(mapFn);
  else if (state.filterTwo) return lists.two.map(mapFn);
  return [];
}

```
---
## The possibilities are endless. Unix pipe ftw

```bash
$ tape test/*.js # run all tests in this directory
```
```bash
$ browserify test/*.js > bundle.js | testling  # run tests in browser with testling
```
```bash
$ browserify -t coverify test.js | testling | coverify # coverify will help you!

TAP version 13
# beep boop
ok 1 should be equal

1..1
# tests 1
# pass  1

# ok

# /tmp/example/test.js: line 7, column 16-28

  if (err) deadCode();
           ^^^^^^^^^^^
```
---
class: center, middle

# A Node-centric testing workflow
aka almost done yall!
<p class="img-cont">
<img src="http://media3.giphy.com/media/TNQHoWzmW8h9K/200.gif" />
</p>

---
# Zuul

"Don't just claim your js supports 'all browsers', prove it with tests!"

<p class="img-cont">
<img src="https://f.cloud.github.com/assets/71256/1669799/fb463296-5c81-11e3-818a-26776dc7a256.jpg" />
</p>
---
## Zuul Basics

Install
```bash
$ npm install zuul -g
```
Run tests locally in the browser. Helpful for debugging!
```bash
$ zuul --local 9000 -- ./test/*.js

open the following url in a browser:
http://localhost:9000/__zuul
```
Run tests in the headless browser phantomjs
```bash
$ zuul --phantomjs  -- ./test/*.js
```
---
## Zuul + Saucelabs

```yaml
# app_directory/.zuul.yml
ui: tape
browserify:
  - transform: reactify
browsers:
  # your browsers here, for example:
  - name: chrome
    version: latest
```

```yaml
# ~/.zuulrc
sauce_username: username
sauce_key: sauce_key
```

<p class="img-cont">
<img width="400" src="https://www.evernote.com/shard/s471/sh/22ac43d5-3a5f-4588-8010-34213bf63ada/986ca65f91163f032d39559a96631b15/deep/0/substack-tape.png" />
</p>

---
# Putting it all together with npm!

A _super chill_ npm workflow
package.json
```json
{
  ...
  "scripts": {
    "postinstall": "npm test",
    "test": "./node_modules/zuul/bin/zuul.js -- ./test/*.js",
    "test-headless": "./node_modules/zuul/bin/zuul.js --phantomjs -- ./test/*.js",
    "test-local": "./node_modules/zuul/bin/zuul.js --local 9000 -- ./test/*.js"
  }
  ...
}
```
---
class: middle, center

# Thanks!

### Amadeus Junqueira

twitter: [@_4m4deus](https://twitter.com/_4m4deus)

blarg: [www.rippityrippity.me](http://rippityrippity.me/)

