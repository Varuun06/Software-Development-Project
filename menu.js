document.addEventListener("DOMContentLoaded", function(){
    var selectedItems = [];
    var buttonEL = document.querySelector("#button-el");
    var priceEL = document.querySelector("#price-el")

    buttonEL.addEventListener("click", function(){
        console.log("Called");
        getPrice(selectedItems);
    });

    function updateCost(price){
        priceEL.textContent = "$"+price;
    }

    function getPrice(selectedItems){
        console.log(selectedItems);
        fetch('/menu', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                items: selectedItems
            })
        })
        .then(response => response.json()) 
        .then(data => {
            updateCost(data);
        });
    }

    // Event delegation for checkbox clicks
    document.querySelector('.tree').addEventListener('change', function(event) {
        if (event.target.matches('input[type="checkbox"]')) {
            insert(event.target.value);
        }
    });

    // Function to insert or remove items from the selectedItems array
    function insert(value) {
        var index = selectedItems.indexOf(value);
        if (index !== -1) {
            selectedItems.splice(index, 1); // Remove item if already selected
        } else {
            selectedItems.push(value); // Add item if not selected
        }
    }


    // Ensure initial visibility state
    document.querySelectorAll('.tree ul').forEach(function(ul) {
        ul.style.display = 'none';
    });

    // Show the root menu
    document.querySelector('.tree > ul').style.display = 'block';
});

// Function to toggle visibility of submenu
    function toggleVisibility(event) {
        event.preventDefault();
        var parent = event.target.parentElement;
        var subMenu = parent.querySelector('ul');
        if (subMenu) {
            subMenu.style.display = subMenu.style.display === 'none' ? 'block' : 'none';
        }
    }
