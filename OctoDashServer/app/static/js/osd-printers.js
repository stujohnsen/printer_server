"use strict()";

var printers = [];

// Global functions
function addPrinter(printer) {
    printers.push(printer);
}

function deletePrinter(printer) {
    for (i=0; i<printers.length; i++) {
        if (printers[i].id == printer.id)
            printers.splice(i, 1);  //Delete the printer without leaving a hole
    }
}

function getPrinterByPrinterId(id) {
    for (var i = 0; i < printers.length; i++) {
        if (printers[i].id == Number(id))
            return printers[i];
    }
    return null;
}

function getPrinterByModuleId(id) {
    id = Number(id) - 1;
    if(printers.length > Number(id))
        return printers[id];
    else
        return null;
}

// function printerAlreadyExists(id) {
//     for(var printerNum=0; printerNum<printers.length; printerNum++) {
//         if(printers[printerNum].id == printer.id){
//             return true;
//         }
//     }
//     return false;
// }
