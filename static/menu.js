document.addEventListener("DOMContentLoaded", function() {
    var selectedItems = [];
    var buttonEL = document.querySelector("#button-el");
    var priceEL = document.querySelector("#price-el");

    buttonEL.addEventListener("click", function() {
        getPrice(selectedItems);
    });

    function updateCost(price) {
        priceEL.textContent = "₹" + price;
    }

    function getPrice(selectedItems) {
        fetch('/calculate_cost', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ items: selectedItems })
        })
        .then(response => response.json())
        .then(data => {
            updateCost(data);
        });
    }

    document.querySelector('.tree').addEventListener('change', function(event) {
        if (event.target.matches('input[type="checkbox"]')) {
            insert(event.target.value);
        }
    });

    function insert(value) {
        var index = selectedItems.indexOf(value);
        if (index !== -1) {
            selectedItems.splice(index, 1);
        } else {
            selectedItems.push(value);
        }
    }

    document.querySelectorAll('.tree ul').forEach(function(ul) {
        ul.style.display = 'none';
    });

    document.querySelector('.tree > ul').style.display = 'block';
});

function toggleVisibility(event) {
    event.preventDefault();
    var parent = event.target.parentElement;
    var subMenu = parent.querySelector('ul');
    if (subMenu) {
        subMenu.style.display = subMenu.style.display === 'none' ? 'block' : 'none';
    }
}


