$('#schedule').click(function(){
    var submitUrl = $(this).data('submit');

    var l1 = $('<label>').attr('class', 'col-sm-2 control-label').html('Email');
    var i1 = $('<div>').attr('class', 'col-sm-10').append($('<input>').attr('type', 'email').attr('class', 'form-control').attr('name', 'email').attr('value', request.email));
    var r1 = $('<div>').attr('class', 'form-group').append(l1).append(i1);

    var l1p = $('<label>').attr('class', 'col-sm-2 control-label').html('Totals');
    var s1p = $('<select>').attr('class', 'form-control').attr('name', 'totals');
    [['sum', 'Sum'], ['no', 'Hide']].forEach(function(val){
        s1p.append($('<option>').attr('value', val[0]).html(val[1]));
    });
    var i1p = $('<div>').attr('class', 'col-sm-10').append(s1p);
    var r1p = $('<div>').attr('class', 'form-group').append(l1p).append(i1p);

    var l2 = $('<label>').attr('class', 'col-sm-2 control-label').html('Time');
    var s2 = $('<select>').attr('class', 'form-control').attr('name', 'time');
    [
        ['coffee', 'Morning (8am)'],
        ['morning', 'Morning (10am)'],
        ['afternoon', 'Afternooon (2pm)'],
        ['evening', 'Evening (6pm)'],
        ['tester', 'Tester'],
    ].forEach(function(val){
        s2.append($('<option>').attr('value', val[0]).html(val[1]));
    });
    var i2 = $('<div>').attr('class', 'col-sm-10').append(s2);
    var r2 = $('<div>').attr('class', 'form-group').append(l2).append(i2);

    var l3 = $('<label>').attr('class', 'col-sm-2 control-label').html('Frequency');
    var s3 = $('<select>').attr('class', 'form-control').attr('name', 'frequency');
    [['daily', 'Daily'], ['weekly', 'Weekly'], ['monthly', 'Monthly']].forEach(function(val){
        s3.append($('<option>').attr('value', val[0]).html(val[1]));
    });
    var i3 = $('<div>').attr('class', 'col-sm-10').append(s3);
    var r3 = $('<div>').attr('class', 'form-group').append(l3).append(i3);

    function updateFreq(){
        $('#freqOptions').remove();
        var v3 = $(this).val();
        var l4 = $('<label>').attr('class', 'col-sm-2 control-label').html('Options');
        var s4 = $('<select>').attr('name', 'options[]');
        var i4 = $('<div>').attr('class', 'col-sm-10').append(s4);
        var r4 = $('<div>').attr('class', 'form-group').append(l4).append(i4).attr('id', 'freqOptions');
        if (v3 == 'weekly') {
            var c41 = [['1', 'Monday'], ['2', 'Tuesday'], ['3', 'Wednesday'], ['4', 'Thursday'], ['5', 'Friday'], ['6', 'Saturday'], ['0', 'Sunday']];
            c41.forEach(function(val){
                s4.append($('<option>').attr('value', val[0]).html(val[1]));
            });
            s4.attr('multiple', 'multiple');
            s4.selectize();
            form.append(r4);
        } else if (v3 == 'monthly') {
            var c42 = Array.apply(null, Array(31)).map(function (_, i) {return ['' + (i + 1), '' + (i + 1)];});
            c42.forEach(function(val){
                s4.append($('<option>').attr('value', val[0]).html(val[1]));
            });
            s4.attr('class', 'form-control');
            form.append(r4);
        }
    }
    s3.change(updateFreq);
    var form = $('<form>').attr('class', 'form-horizontal').append(r1).append(r1p).append(r2).append(r3);
    var submitButton = $('<button>').html('Save').attr('class', 'btn btn-primary');
    var footer = $('<div>').append(submitButton);
    var modal = newModal('Schedule an email', form, footer);
    submitButton.click(function(){
        $.ajax({
            url: submitUrl,
            data: form.serialize(),
            type: 'post',
            success: function(data){
                modal.modal('hide');
                var alert = $('<div>').addClass('alert alert-danger toast').attr('role', 'alert').html('Auto emails have been scheduled');
                setTimeout(function(){ alert.remove(); }, 5000);
                $('body').append(alert.fadeIn());
            },
            error: function(err) {
                console.log(err);
            }
        })
    });
    return false;
});