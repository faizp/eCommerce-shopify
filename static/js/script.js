$('#btn').click(function () {
    var username = $('#username').val()
    var password = $('#password').val()
    var data = {
        'csrfmiddlewaretoken': '{{csrf token}}',
        'username': username,
        'password': password
    }
    if (username == "") {
        $('#invalid').html("The username that you've entered doesn't match any account")
    } else if (password == "") {
        $('#invalid').html("The password you have entered is incorrect")
    } else {
        $.ajax({
            url: '/login/',
            method: 'POST',
            data: data,
            dataType: 'json',
            success: function (data) {
                if (data == 'true') {
                    window.location.replace('/')
                }
                if (data == 'false') {
                    $('#invalid').html("Please enter a valid username and password")
                }
            }
        })
    }
})


function addToCart (id) {
    $.ajax({
            url: '/add_cart/'+id,
            method: 'POST',
        })
}

$(document).ready(function(){
    $('#add-to-cart').click(function(){
        $('#alert').show()
    })
});


function addQuantiy(id) {
    $.ajax({

    })

}

    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                $('#image1').attr('src', e.target.result);
            }

            reader.readAsDataURL(input.files[0]);
        }
    }

    $("#image1").change(function(){
        readURL(this);
    });

