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


function addToCart(id) {
    $.ajax({
        url: '/add_cart/' + id,
        method: 'POST',
    })
}


function addQuantity(id) {
    $.ajax({
        url: '/add_quantity/' + id,
        method: 'POST',
        success: function (data) {
            $('#'+id+'-quantity').html(data.quantity);
            console.log(data.total)
            $('#'+id+'-price').html(data.total)
        }
    })
}


function reduceQuantity(id) {
    $.ajax({
        url: '/reduce_quantity/' + id,
        method: 'POST',
        success: function (data) {
            $('#'+id+'-quantity').html(data.quantity)
            $('#'+id+'-price').html(data.total)
        }
    })

}

