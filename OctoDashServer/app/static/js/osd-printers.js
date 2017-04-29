"use strict()";

// Global printer list. Contains all printer instances.
// TODO Could make this a "class" like printer is, with prototype functions.
var printers = [];


// Add a printer object to the printers list
function addPrinter(printer) {
    printers.push(printer);
}

// Delete a printer from the printers list
function deletePrinter(printer) {
    for (i=0; i<printers.length; i++) {
        if (printers[i].id == printer.id)
            printers.splice(i, 1);  //Delete the printer without leaving a hole
    }
}

// Get printer from the printerId
function getPrinterByPrinterId(id) {
    for (var i = 0; i < printers.length; i++) {
        if (printers[i].id == Number(id))
            return printers[i];
    }
    return null;
}

// Get printer from the moduleId
function getPrinterByModuleId(id) {
    id = Number(id) - 1;
    if(printers.length > Number(id))
        return printers[id];
    else
        return null;
}

// Jump through the printer array and update the snapshot view for each
function updateSnapshotViews() {
    for (var printer in printers) {
        var printerModule = printers[printer].printerModule;
        printerModule.updateSnapshotView();
    }
}
