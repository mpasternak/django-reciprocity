QUnit.module('Test Module', {   
    beforeEach: function () {
        sinon.replace(jQuery.fn, 'loadTemplate',  sinon.stub());
	iplweb.reciprocity.init("token", "prefix", "../../doesntmatter/");
    },
    afterEach: function () {
	sinon.restore();
    }
});

QUnit.test('check connect', function(assert){
    iplweb.reciprocity.pushstream = sinon.createStubInstance(PushStream, {
	connect: sinon.stub()
    });
    iplweb.reciprocity.connect();
    assert.equal(iplweb.reciprocity.pushstream.connect.called, true);
});

QUnit.test('check onError', function(assert) {
    assert.equal(iplweb.reciprocity.loadingFailed, false);
    
    iplweb.reciprocity.onError({type: "load"});
    assert.equal(jQuery.fn.loadTemplate.called, true);
    
    assert.equal(iplweb.reciprocity.loadingFailed, true);
});

