QUnit.module('Test Module', {
    beforeEach: function () {
        sinon.replace(jQuery.fn, 'loadTemplate', sinon.stub());
        iplweb.reciprocity.init("token", "prefix", "../../doesntmatter/");
        iplweb.reciprocity.pushstream = sinon.createStubInstance(PushStream, {
            connect: sinon.stub(),
            addChannel: sinon.stub()
        });
    },
    afterEach: function () {
        sinon.restore();
    }
});

QUnit.test('reciprocity.connect', function (assert) {
    iplweb.reciprocity.connect();
    assert.equal(iplweb.reciprocity.pushstream.connect.called, true);
});

QUnit.test('reciprocity.onError', function (assert) {
    assert.notOk(iplweb.reciprocity.loadingFailed);
    iplweb.reciprocity.onError({type: "load"});
    assert.ok(jQuery.fn.loadTemplate.called);
    assert.ok(iplweb.reciprocity.loadingFailed);
});

QUnit.test('reciprocity.subscribe', function (assert) {
    iplweb.reciprocity.subscribe('foo');
    assert.ok(iplweb.reciprocity.pushstream.addChannel.called);
});

QUnit.test('reciprocity.callout', function (assert) {
    iplweb.reciprocity.callout({
        "class": "success",
        "header": "header",
        "body": "body"
    });
    assert.ok(jQuery.fn.loadTemplate.called);
});


QUnit.test('reciprocity.calloutWithLink', function (assert) {
    iplweb.reciprocity.calloutWithLink({
        "class": "success",
        "header": "header",
        "body": "body",
        "href": "lel"
    });
    assert.ok(jQuery.fn.loadTemplate.called);
});
