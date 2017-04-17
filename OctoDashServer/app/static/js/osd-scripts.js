/*jshint esversion: 6 */
"use strict()";

/* The second level object is any object like a modal or overlay that is "above"
 * the regular page. Clicking on anything that is not this object will cause
 * the object to close. This makes it so only one modal or menu item can be
 * active at a time, and is much cheaper than scanning through all items
 * whenever a click occurs to see if they are active and disable them.
 */
var activeSecondLevelObject = null;
var activeSecondLevelController = null;
var socket;
const numTimesToRetrySocketBeforeError = 10;
var timesRetried = 0;
var timeout;
const timeoutInterval = 5000; //ms

// Set snapshot update interval
window.setInterval(updateSnapshotViews, 3000);

function createNavBar() {
    var navBar = document.getElementById("nav_bar");

    var heroLogo = document.createElement("IMG");
    heroLogo.className = "hero_logo";
    heroLogo.id = "hero_logo";
    heroLogo.src = "../../static/img/uofulogo.png";

    navBar.appendChild(heroLogo);
}

function createOctoSlackModal() {
    // Create elements
    var octoSlackModal = document.getElementById("octo_slack_modal");

    var modalContent = document.createElement("DIV");
    modalContent.className = "octo_slack_modal_content";
    modalContent.id = "octo_slack_modal_content";
    octoSlackModal.appendChild(modalContent);

    var iframe = document.createElement("IFRAME");
    iframe.id = "octo_slack_modal_iframe";

    modalContent.appendChild(iframe);
}

function createSnapshotModal() {
    var snapshotModal = document.getElementById("snapshot_modal");

    var modalContent = document.createElement("DIV");
    modalContent.className = "snapshot_modal_content";
    modalContent.id = "snapshot_modal_content";
    snapshotModal.appendChild(modalContent);

    var snapshotImage = document.createElement("IMG");
    snapshotImage.id = "snapshot_modal_image";
    snapshotImage.src = "img/offline.png";

    modalContent.appendChild(snapshotImage);
}

function displayOctoSlackModal(printerId) {
    // Set the modal iframe source to be the appropriate URL
    var printer = getPrinterByPrinterId(printerId);
    var modalIframe = document.getElementById("octo_slack_modal_iframe");
    modalIframe.src = printer.octoprintUrl;

    // Display the modal
    var octoSlackModalContent = document.getElementById("octo_slack_modal_content");
    octoSlackModalContent.style.display = "block";
    var octoSlackModal = document.getElementById("octo_slack_modal");
    octoSlackModal.style.display = "block";

    // Keep the snapshots from updating while the modal is active
    shouldUpdateSnapshots = false;

}

function hideOctoSlackModal() {
    // Stop any large images or streams
    window.stop();

    // Set the modal iframe source to be the appropriate URL
    var modalIframe = document.getElementById("octo_slack_modal_iframe");
    modalIframe.src = "about:blank";

    // Display the modal
    var octoSlackModalContent = document.getElementById("octo_slack_modal_content");
    octoSlackModalContent.style.display = "none";
    var octoSlackModal = document.getElementById("octo_slack_modal");
    octoSlackModal.style.display = "none";

    // Keep the snapshots from updating while the modal is active
    shouldUpdateSnapshots = true;
}

function displaySnapshotModal(printerId) {
    // Rotate the container to match the set rotation of the static snapshot
    var snapshot = document.getElementById("snapshot_" + printerId);
    var angle = snapshot.title; //Title contains angle
    var modalContent = document.getElementById("snapshot_modal_content");
    modalContent.style.webkitTransform = "rotate("+angle+"deg)";

    // Set the modal image source to be the appropriate webcam feed
    var printer = getPrinterByPrinterId(printerId);
    var modalImage = document.getElementById("snapshot_modal_image");
    modalImage.src = printer.octoprintWebcamLiveUrl;

    // Display the modal
    var snapshotModal = document.getElementById("snapshot_modal");
    snapshotModal.style.display = "block";
    modalContent.style.display = "inline-block";

    // Keep the snapshots from updating while the modal is active
    shouldUpdateSnapshots = false;
}

function hideSnapshotModal() {
    // Stop any large images or streams
    window.stop();

    var modalImage = document.getElementById("snapshot_modal_image");
    modalImage.src = "img/offline.png";

    // Display the modal
    var snapshotModal = document.getElementById("snapshot_modal");
    snapshotModal.style.display = "none";
    var modalContent = document.getElementById("snapshot_modal_content");
    modalContent.style.display = "none";

    // Keep the snapshots from updating while the modal is active
    shouldUpdateSnapshots = true;
}

function createSecondLevelObjectEventListeners() {
    $(window).on("click" , function(event) {
        var clickedObject = event.target;
        var printerId;  // Needs to be defined here for hoisting. Stupid JSHint...
        var overlay;    // Needs to be defined here for hoisting. Stupid JSHint...

        /* ACTIVE SECOND-LEVEL OBJECT */
        if (activeSecondLevelObject !== null &&
            clickedObject !== activeSecondLevelObject &&
            !$.contains(activeSecondLevelObject, clickedObject) &&
            clickedObject !== activeSecondLevelController)
        {
            activeSecondLevelObject.style.display = "none";
            activeSecondLevelObject = null;
            activeSecondLevelController = null;

            if (clickedObject.id == "snapshot_modal") {
                hideSnapshotModal();
            }
            else if(clickedObject.id == "octo_slack_modal") {
                hideOctoSlackModal();
            }
        }
        /* BUTTONS */
        else if (clickedObject.className.includes("settings_icon")) {
            printerId = event.target.id.replace("settings_icon", "");
            overlay = document.getElementById("settings_overlay" + printerId);

            if (clickedObject === activeSecondLevelController) {
                overlay.style.display = "none";
                activeSecondLevelController = null;
                activeSecondLevelObject = null;
            }
            else {
                overlay.style.display = "block";
                activeSecondLevelObject = overlay;
                activeSecondLevelController = clickedObject;
            }
        }
        else if (clickedObject.className.includes("info_icon")) {
            printerId = event.target.id.replace("info_icon", "");
            overlay = document.getElementById("info_overlay" + printerId);

            if (clickedObject === activeSecondLevelController) {
                overlay.style.display = "none";
                activeSecondLevelController = null;
                activeSecondLevelObject = null;
            }
            else {
                overlay.style.display = "block";
                activeSecondLevelObject = overlay;
                activeSecondLevelController = clickedObject;
            }
        }
        /* MODALS */
        // This is a button, but the controller is unclickable while it is up.
        // It counts as a modal
        else if (clickedObject.className.includes("printer_icon")) {
            printerId = event.target.id.replace("printer_icon_", "");
            activeSecondLevelObject = document.getElementById("octo_slack_modal_content");
            activeSecondLevelController = clickedObject;
            displayOctoSlackModal(Number(printerId));
        }
        else if (clickedObject.className.includes("snapshot")) {
            printerId = event.target.id.replace("snapshot_", "");
            activeSecondLevelObject = document.getElementById("snapshot_modal_content");
            activeSecondLevelController = clickedObject;
            displaySnapshotModal(Number(printerId));
        }
    });
}

function updateSnapshotViews() {
    for (var printer in printers) {
        var printerModule = printers[printer].printerModule;
        printerModule.updateSnapshotView();
    }
}

function startWebSocket(url) {
    // Let's open a web socket
    socket = new SockJS(url);

    socket.onopen = function(event) {
        // Web Socket is connected
        console.log("Server socket connect successful.");
        timesRetried = 0;
    };

    socket.onmessage = function (event) {
        // Web Socket received message
        var payload = JSON.parse(event.data);
        var message = payload.message;
        var numPrintersToAdd = payload.num_printers;
        var printerId;
        var printerObject;

        // Printer setup occurs on server connect
        if(payload.message_type == "on_server_connect") {
            for (var printerDef in message) {
                // Check if printer already exists (happens on socket reconnect)
                printerId = message[printerDef].printer_id;
                if(getPrinterByPrinterId(printerId) !== null){
                    return;
                }

                // Else create new printer
                var type = message[printerDef].printer_type;
                var name = message[printerDef].printer_name;
                var url = message[printerDef].url;
                printerObject = new printer(printerId, name, type, url);

                // Rotate the snapshot to the angle defined in the database
                var angle = message[printerDef].camera_rotation % 360;  // Get it in standard angle range
                var timesToRotate = Math.floor(angle / 90); // Number of times to rotate by 90
                for(var rotationCount=0; rotationCount<timesToRotate; rotationCount++) {
                    if(angle > 0) {
                        printerObject.printerModule.rotateSnapshotRight90Deg(angle);
                    }
                    else {
                        printerObject.printerModule.rotateSnapshotLeft90Deg(angle);
                    }
                }
            }
        }
        //Printer updates occur on all other types of messages
        //connected: apikey, version. branch, display_version, plugin_hash, config_hash
        else if(payload.message_type == "connected") {
            printerObject = getPrinterByPrinterId(payload.printer_id);
            if(printerObject !== null && printerObject !== undefined) {
                printerObject.onSocketConnect(message);
            }
        }
        // current: state, job, progress, currentZ, offsets, temps, logs, messages
        else if(payload.message_type == "current") {
            printerObject = getPrinterByPrinterId(payload.printer_id);
            if(printerObject !== null && printerObject !== undefined) {
                printerObject.onSocketReceiveCurrent(message);
            }
        }
        // history: state, job, progress, currentZ, offsets, temps, logs, messages
        else if(payload.message_type == "history") {
            printerObject = getPrinterByPrinterId(payload.printer_id);
            if(printerObject !== null && printerObject !== undefined) {
                printerObject.onSocketReceiveHistory(message);
            }
        }
        // event: type, payload
        else if(payload.message_type == "event") {
            printerObject = getPrinterByPrinterId(payload.printer_id);
            if(printerObject !== null && printerObject !== undefined) {
                printerObject.onSocketReceiveEvent(message);
            }
        }
        // slicingProgress: slicer, source_location, source_path, dest_location, dest_path, progress
        else if(payload.message_type == "slicingProgress") {
            printerObject = getPrinterByPrinterId(payload.printer_id);
            if(printerObject !== null && printerObject !== undefined) {
                printerObject.onSocketReceiveSlicingProgress(message);
            }
        }
        // plugin: messages generated by plugins. Plugin-specific.
        else if(payload.message_type == "plugin") {
            printerObject = getPrinterByPrinterId(payload.printer_id);
            if(printerObject !== null && printerObject !== undefined) {
                printerObject.onSocketReceivePluginMessage(message);
            }
        }
        else {
            // Unknown payload type
            console.error("Unknown payload type detected. Check Octoprint docs for info on new type.");
        }

        // TODO Remove this line after testing
        // document.getElementById("test_area").innerHTML = JSON.stringify(message);
    };

    socket.onclose = function(event) {
        // Web Socket is closed. Display error state on printer modules
        for(var printer in printers) {
            var printerModule = printers[printer].printerModule;
            printerModule.DOM.className = "printer_module error";
        }

        // Try to reconnect
        if(timesRetried <= numTimesToRetrySocketBeforeError) {
            console.error("Socket connection closed. Trying to reconnect.");
            timeout = setTimeout(reconnectSocket, timeoutInterval);
        }
        else {
            console.error("Socket connection could not be reestablished. Please refresh the page.");
        }
    };
}

function reconnectSocket() {
    timesRetried = timesRetried + 1;
    startWebSocket(socket.url);
}

// http://stackoverflow.com/questions/6312993/javascript-seconds-to-time-string-with-format-hhmmss
String.prototype.toHHMMSS = function() {
    var sec_num = parseInt(this, 10); // don't forget the second param
    var hours   = Math.floor(sec_num / 3600);
    var minutes = Math.floor((sec_num - (hours * 3600)) / 60);
    var seconds = sec_num - (hours * 3600) - (minutes * 60);

    if (hours   < 10) {hours   = "0"+hours;}
    if (minutes < 10) {minutes = "0"+minutes;}
    if (seconds < 10) {seconds = "0"+seconds;}
    return hours+':'+minutes+':'+seconds;
};

String.prototype.toHHMM = function() {
    var sec_num = parseInt(this, 10); // don't forget the second param
    var hours   = Math.floor(sec_num / 3600);
    var minutes = Math.floor((sec_num - (hours * 3600)) / 60);

    if (hours   < 10) {hours   = "0"+hours;}
    if (minutes < 10) {minutes = "0"+minutes;}
    return hours+':'+minutes;
};
