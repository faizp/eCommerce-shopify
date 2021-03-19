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
    console.log(id)
    var size = $('#size').val();
    $.ajax({
        url: '/add_cart/' + id,
        method: 'POST',
        data: {'size': size},
        dataType: 'json',
        success: function () {
            $('.js-addcart-detail').each(function () {
                var nameProduct = $(this).parent().parent().parent().parent().find('.js-name-detail').html();
                $(this).on('click', function () {
                    swal(nameProduct, "is added to cart !", "success");
                });
            });
        }
    })
}


function addProduct() {
        var id = $('#product-id').val()
        var size = $('#product-size').val();
    $.ajax({
        url: '/add_cart/' + id,
        method: 'POST',
        data: {'size': size},
        dataType: 'json',
        success: function () {
            $('.js-addcart-detail').each(function () {
                var nameProduct = $(this).parent().parent().parent().parent().find('.js-name-detail').html();
                $(this).on('click', function () {
                    swal(nameProduct, "is added to cart !", "success");
                });
            });
        }
    })
    }


function removeFromCart(id) {
    $.ajax({
        url: '/remove_from_cart/' + id,
        method: 'POST',
        success: function (data) {
            if (data == 'true') {
                $('#' + id + '-cart').remove()
            }
        }
    })

}


function addQuantity(id) {
    $.ajax({
        url: '/add_quantity/' + id,
        method: 'POST',
        success: function (data) {
            if (data == 'false') {
                $('.js-addcart-detail').each(function () {
                    $(this).on('click', function () {
                        swal("is added to cart !", "success");
                    });
                });
            } else {
                $('#' + id + '-quantity').val(data.quantity);
                console.log(data.total)
                $('#' + id + '-price').html(data.item_total)
                $('#total-amount').html(data.total)
            }
        }
    })
}


function reduceQuantity(id) {
    $.ajax({
        url: '/reduce_quantity/' + id,
        method: 'POST',
        success: function (data) {
            if (data.quantity <= 1) {
                window.location.reload()
            }
            $('#' + id + '-quantity').html(data.quantity)
            $('#' + id + '-price').html(data.item_total)
            $('#total-amount').html(data.total)
        }
    })
}


