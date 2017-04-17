/*jshint esversion: 6 */
"use strict()";

var printer = function (id, name, type, url) {
     if (name !== undefined && typeof(name)==='string' &&
         type !== undefined && typeof(type)==='string' ) {
        this.id = id;
        this.name = name;
        this.type = type;
        this.octoprintUrl = url;
        this.octoprintWebcamLiveUrl = this.octoprintUrl + "/webcam/?action=stream";
        this.octoprintWebcamSnapshotUrl = this.octoprintUrl + "/webcam/?action=snapshot";
        this.printerModule = new printerModule(this);
    }
    else {
        // If there are any errors in the input then put in a null printer
        this.id = null;
        this.name = null;
        this.type = null;
        this.octoprintUrl = null;
        this.octoprintWebcamLiveUrl = null;
        this.octoprintWebcamSnapshotUrl = null;
        this.octoPrintClient = null;
        this.printerModule = null;
    }

    // Add this to the list of active printers
    addPrinter(this);
};

// Printer Function Definitions
printer.prototype.onSocketConnect = function(message) {
    console.log(this.name + " socket connected successfully.");
};

printer.prototype.onSocketReceiveCurrent = function(message) {
    // console.log(this.name + " received a current message.");
    this.printerModule.updatePrinterStatus(message);
};

printer.prototype.onSocketReceiveHistory = function(message) {
    // console.log(this.name + " received a history message.");
};

printer.prototype.onSocketReceiveEvent = function(message) {
    // console.log(this.name + " received an event message.");
};

printer.prototype.onSocketReceiveSlicingProgress = function(message) {
    // console.log(this.name + " received a slicing progress message.");
};

printer.prototype.onSocketReceivePluginMessage = function(message) {
    // console.log(this.name + " received a plugin message.");
};
