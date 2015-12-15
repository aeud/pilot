newModal = function(title, body, footer, size){
    var size = size || 'lg';
    var modal = $('<div>').attr('class', 'modal fade');
    var modalDialog = $('<div>').attr('class', 'modal-dialog').addClass('modal-' + size);
    var modalContent = $('<div>').attr('class', 'modal-content');
    var modalHeader = $('<div>').attr('class', 'modal-header');
    var closeButton = $('<button>').attr('class', 'close').attr('aria-label', 'Close').attr('data-dismiss', 'modal').append($('<span>').attr('aria-hidden', 'true').html('&times;'));
    var modalTitle = $('<h4>').attr('class', 'modal-title').html(title);
    var modalBody = $('<div>').attr('class', 'modal-body').append(body);
    modalHeader.append(closeButton);
    modalHeader.append(modalTitle);
    modalContent.append(modalHeader);
    modalContent.append(modalBody);
    modalDialog.append(modalContent);
    if (typeof footer != 'undefined' && footer) {
        var modalFooter = $('<div>').attr('class', 'modal-footer').html(footer);
        modalContent.append(modalFooter);
    }
    modal.append(modalDialog);
    modal.modal();
    return modal;
}