var iplweb = iplweb || {};

iplweb.reciprocity = iplweb.reciprocity || {};

iplweb.reciprocity.init = function (csrftoken, pubPrefix, templatePath, host, port, useSSL) {
    this.csrftoken = csrftoken;
    this.pubPrefix = pubPrefix;

    if (host === null)
        host = window.location.hostname;

    if (port === null || port === '')
        port = window.location.port;

    if (useSSL === null) {
        useSSL = false;

        if (window.location.protocol === 'https:')
            useSSL = true;
    }

    this.pushstream = new PushStream({
        host: host,
        port: port,
        modes: "websocket",
        useSSL: useSSL,
        onmessage: this.onMessage.bind(this),
        onerror: this.onError.bind(this)
    });

    this.templatePath = templatePath;
    this.loadingFailed = false;
};

iplweb.reciprocity.connect = function () {
    this.pushstream.connect();
};

iplweb.reciprocity.onError = function (eventType) {
    if (eventType.type == "load" && !this.loadingFailed) {
        iplweb.reciprocity.callout({
            header: "Cannot connect to notification server",
            body: "The notification server seems to be unavailable.",
            class: "alert"
        });
        this.loadingFailed = true;
    }
};


iplweb.reciprocity.subscribe = function (channel) {
    return this.pushstream.addChannel(this.pubPrefix + channel);
};

iplweb.reciprocity.callout = function (message) {
    var span = $("<div style='display: none;'/>").loadTemplate(this.templatePath + "callout.html",
        {
            "class": message.class,
            "header": message.header,
            "body": message.body
        }
    );

    $("#reciprocity-callout-placeholder").append(span);
    Foundation.Motion.animateIn(span, "slide-in-left");
};

iplweb.reciprocity.calloutWithLink = function (message) {
    $("#reciprocity-callout-placeholder").append(
        $("<span/>")
            .loadTemplate(
                this.templatePath + "callout-with-link.html",
                {
                    "class": message.class,
                    "header": message.header,
                    "body": message.body,
                    "href": message.href
                }
            )
    );
};

iplweb.reciprocity.gotoPage = function (message) {
    $("html").fadeOut("slow", function () {
        location.href = message.href;
    });
};

iplweb.reciprocity.modalDialog = function (message) {
    $("#reciprocity-dialog-placeholder")
        .loadTemplate(
            this.templatePath + "modal-dialog.html",
            {
                "header": message.header,
                "lead": message.lead,
                "paragraph": message.paragraph
            },
            {
                "success": function () {

                    $("#reciprocity-modal-dialog")
                        .foundation()
                        .foundation("open");

                }
            });
};

iplweb.reciprocity.pleaseWaitDialog = function (message) {
    $("#reciprocity-dialog-placeholder")
        .loadTemplate(
            this.templatePath + "please-wait-dialog.html",
            {
                "header": message.header,
                "lead": message.lead,
                "paragraph": message.paragraph
            },
            {
                "success": function () {
                    $("#reciprocity-please-wait-dialog")
                        .foundation()
                        .foundation("open");
                }
            });
};

iplweb.reciprocity.progressDialogInit = function (message) {
    $("#reciprocity-dialog-placeholder")
        .loadTemplate(
            this.templatePath + "progress-dialog.html",
            {
                "header": message.header,
                "lead": message.lead,
                "paragraph": message.paragraph
            },
            {
                "success": function () {
                    $("#reciprocity-progress-dialog")
                        .foundation()
                        .foundation("open");
                }
            });
};

iplweb.reciprocity.progressDialogUpdate = function (message) {
    var percent = message.value + "%";
    $("#reciprocity-progress-meter").css("width", percent);
    $("p", $("#reciprocity-progress-meter")).text(percent);
};

iplweb.reciprocity.onMessage = function (message) {

    if (!message.type) {
        console.log("iplweb.reciprocity.onMessage: received message without 'type' specified: ", message);
        return;
    }

    switch (message.type) {
        case "callout":
            iplweb.reciprocity.callout(message);
            break;

        case "callout-with-link":
            iplweb.reciprocity.calloutWithLink(message);
            break;

        case "goto-page":
            iplweb.reciprocity.gotoPage(message);
            break;

        case "modal-dialog":
            iplweb.reciprocity.modalDialog(message);
            break;

        case "please-wait-dialog":
            iplweb.reciprocity.pleaseWaitDialog(message);
            break;

        case "progress-dialog-init":
            iplweb.reciprocity.progressDialogInit(message);
            break;

        case "progress-dialog-update":
            iplweb.reciprocity.progressDialogUpdate(message);
            break;

        case "progress-dialog-close":
            $("#reciprocity-progress-dialog").foundation("close");
            break;

        case "html":
            $(message.selector).html(message.value);
            break;

        case "eval":
            eval(message.value);
            break;

        case "close-modal-dialog":
            $("#reciprocity-modal-dialog").foundation("close");
            break;

        case "close-please-wait-dialog":
            $("#reciprocity-please-wait-dialog").foundation("close");
            break;

        case "debug":
            console.log(message);
            break;

        default:
            console.log('iplweb.reciprocity.onMessage: received message with unsupported type: ' + message.type);
            break;
    }
    ;

};
