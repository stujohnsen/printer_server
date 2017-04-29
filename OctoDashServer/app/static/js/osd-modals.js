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

// Creates the modal that houses the Octoprint website
// Note that there is only one of these modals on the site
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

// Creates the modal that houses the webcam live feed
// Note that there is only one of these modals on the site
function createSnapshotModal() {
    var snapshotModal = document.getElementById("snapshot_modal");

    var modalContent = document.createElement("DIV");
    modalContent.className = "snapshot_modal_content";
    modalContent.id = "snapshot_modal_content";
    snapshotModal.appendChild(modalContent);

    var snapshotImage = document.createElement("IMG");
    snapshotImage.id = "snapshot_modal_image";
    snapshotImage.src = "{{ url_for('static', filename='img/offline.png') }}";

    modalContent.appendChild(snapshotImage);
}

// Populates the modal and displays it
function displayOctoSlackModal(id) {
    // Set the modal iframe source to be the appropriate URL
    var printer = getPrinterByModuleId(id);
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

// Stops the feed download and hides the modal
function hideOctoSlackModal() {
    // Stop any large images or streams
    window.stop();

    // Set the modal iframe source to be blank.
    // This forces reload of the iframe source each time and keeps
    // old instances from showing up temporarily
    var modalIframe = document.getElementById("octo_slack_modal_iframe");
    modalIframe.src = "about:blank";

    // Hide the modal
    var octoSlackModalContent = document.getElementById("octo_slack_modal_content");
    octoSlackModalContent.style.display = "none";
    var octoSlackModal = document.getElementById("octo_slack_modal");
    octoSlackModal.style.display = "none";

    // Reenable the snapshot updates
    shouldUpdateSnapshots = true;
}

// Populates the modal and shows it
function displaySnapshotModal(id) {
    // Rotate the container to match the set rotation of the static snapshot
    var snapshot = document.getElementById("snapshot_" + id);

    var angle = snapshot.getAttribute("data-rotation-angle"); // img tag contains angle
    var flipHoriz = snapshot.getAttribute("data-horizontal-flip"); // img tag contains angle
    var flipVert = snapshot.getAttribute("data-vertical-flip"); // img tag contains angle
    var transformString = "";

    // Build the transform string
    if(angle != "0") {
        transformString += "rotate("+angle+"deg) ";
    }
    if(flipHoriz == "True") {
        transformString += "rotateY(180deg) ";
    }
    if(flipVert == "True") {
        transformString += "rotateX(180deg) ";
    }

    var modalContent = document.getElementById("snapshot_modal_content");
    modalContent.style.webkitTransform = transformString;

    // Set the modal image source to be the appropriate webcam feed
    var printer = getPrinterByModuleId(id);
    var modalImage = document.getElementById("snapshot_modal_image");
    modalImage.src = printer.octoprintWebcamLiveUrl;

    // Display the modal
    var snapshotModal = document.getElementById("snapshot_modal");
    snapshotModal.style.display = "block";
    modalContent.style.display = "inline-block";

    // Keep the snapshots from updating while the modal is active
    shouldUpdateSnapshots = false;
}

// Changes the modal source to an offline image and hides it
function hideSnapshotModal() {
    // Stop any large images or streams
    window.stop();

    var modalImage = document.getElementById("snapshot_modal_image");
    modalImage.src = "{{ url_for('static', filename='img/offline.png') }}";

    // Hide the modal
    var snapshotModal = document.getElementById("snapshot_modal");
    snapshotModal.style.display = "none";
    var modalContent = document.getElementById("snapshot_modal_content");
    modalContent.style.display = "none";

    // Reenable the snapshots
    shouldUpdateSnapshots = true;
}

// Creates the listeners for second level objects
// A second level object controller is the button that enables the action
// See the explanation at the top of this document to learn more about second level objects
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
