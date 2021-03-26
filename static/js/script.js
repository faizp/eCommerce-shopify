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
        success: function (data) {
            console.log(data.count)
            $('#cart-icon').attr('data-notify', data.count);
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
        success: function (data) {
            console.log(data.count)
            $('#cart-icon').attr('data-notify', data.count);
            var a = $('#cart-icon').attr('data-notify');
            console.log(a)
            $('.js-addcart-detail').each(function () {
                var nameProduct = $(this).parent().parent().parent().parent().find('.js-name-detail').html();
                $(this).on('click', function () {
                    swal(nameProduct, "is added to cart !", "success");
                });
            });
        }
    })
}


// function removeFromCart(id) {
//     $.ajax({
//         url: '/remove_from_cart/' + id,
//         method: 'POST',
//         success: function (data) {
//             console.log(data)
//             if (data == 'true') {
//                 $('#' + id + '-cart').remove()
//             }
//             if (data == 'false') {
//                 console.log('hello')
//                 $('#' + id + '-cart').remove()
//                 window.location.reload()
//             }
//         }
//     })
//
// }


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

$(document).ready(function () {
    $("#form_id").validate({
        errorClass: 'errors',
        rules: {
            discount: {
                required: true
            }
        },
        messages: {
            discount: {
                required: "Please type in a discount",
            }
        }
    });
});


function addOffer() {
    var isvalid = $('#form_id').valid();
    if (isvalid) {
        var category = $('#category').val();
        console.log(category)
        var name = $('#offer-name').val();
        var discount = $('#discount').val();
        var startDate = $('#start-date').val();
        console.log(startDate)
        var endDate = $('#end-date').val();
        console.log(endDate)
        var data = {
            'csrfmiddlewaretoken': '{{ csrf_token }}',
            'category': category,
            'name': name,
            'discount': discount,
            'startDate': startDate,
            'endDate': endDate
        };
        $.ajax({
            url: '/admin/add-offer/',
            method: 'POST',
            data: data,
            dataType: 'json',
            success: function (data) {
                if (data == 'true') {
                    window.location.replace('/admin/offers/')
                }
                if (data == 'false') {
                    console.log('wrong')
                    window.alert('An offer for this category is active right now,  Please choose different category')
                }
                if (data == 'dateError') {
                    window.alert('You have selected invalid Dates')
                }
            }
        })
    }
}