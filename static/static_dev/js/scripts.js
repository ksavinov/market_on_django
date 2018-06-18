$(document).ready(function(){
    var form = $('#form_buying_product');
    console.log(form);
    form.on('submit', function(e){
        e.preventDefault();
        console.log('123');
        var nmb = $('#number').val();
        console.log(nmb);
        var submit_btn = $('#submit_btn');
        var product_id =  submit_btn.data("product_id");
        var name = submit_btn.data("name");
        var price = submit_btn.data("price");
        console.log(product_id );
        console.log(name);

        $('.basket-items ul').append('<li>'+name+', ' + nmb + 'items ' + 'for ' + price + 'RUB  ' +
            '<a class="delete-item" href="">x</a>'+
            '</li>');
    });

    function showingBasket(){
        $('.basket-items').removeClass('hidden');
    };

    $('.basket-container').on('click, hover', function(e){
        e.preventDefault();
        showingBasket();
    });

    $('.basket-container').mouseover(function(){
        showingBasket();
    });

    // $('.basket-container').mouseout(function(){
    //     showingBasket();
    // });

    $(document).on('click', 'delete-item', function(e){
        e.preventDefault();
        $(this).closest('li').remove();
    })
});