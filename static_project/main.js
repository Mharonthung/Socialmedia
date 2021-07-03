$(document).ready(function(){
    $('#modal-btn').click(function(){
      $('.ui.modal')
      .modal('show')
    ;
    });
    $('.ui.dropdown').dropdown()

    $('.message .close')
        .on('click', function() {
            $(this)
                .closest('.message')
                .transition('fade');
  });
})