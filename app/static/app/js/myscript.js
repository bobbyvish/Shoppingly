$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})



let smallImg = document.getElementsByClassName('thumbnail');
let activeImages = document.getElementsByClassName('active');
for (var i = 0; i < smallImg.length; i++){
    smallImg[i].addEventListener('mouseover', function () {
        if (activeImages.length > 0) {
            activeImages[0].classList.remove('active')
        }
        this.classList.add('active')
        document.getElementById('featured').src=this.src
    })
};

let buttonLeft = document.getElementById('slideleft');
let buttonRight = document.getElementById('slideright');
buttonLeft.addEventListener('click', function () {
    console.log('left')
    document.getElementById('slider').scrollLeft -= 50
});

buttonRight.addEventListener('click', function () {
    console.log('right')
    document.getElementById('slider').scrollLeft += 50
});



$('.update_cart').click(function () {
    var id = this.dataset.product
    var action = this.dataset.action
    var eml =this.parentNode.children[2]
    console.log(id, action);
    $.ajax({
        type: "GET",
        url: "/update_item",
        data: {
            prod_id:id,
            action:action
        },
        success: function (data) {

                eml.innerText = data.quantity
                document.getElementById('amount').innerText=data.amount
            document.getElementById('totalamount').innerText = data.total_amount
        }
    })
})


var magnifying_area = document.getElementById('magnifying_area');
var magnifying_img = document.getElementById('feature');

magnifying_area.addEventListener("mouseover", function () {
    magnifying_img.style.transform = 'translate(-50%,-50%) scale(2)'
});

magnifying_img.addEventListener("mouseleave", function () {
    magnifying_img.style.transform = "translate(-50%,-50%) scale(2)"
});