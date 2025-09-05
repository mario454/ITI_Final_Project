"use strict";
console.log("JS file is linked");

const btn = document.getElementById("gototop");
if (btn) {
    window.addEventListener("scroll", () => {
        if (window.scrollY > 200) {
            btn.style.visibility = "visible";
            btn.style.opacity = "1";
        } else {
            btn.style.visibility = "hidden";
            btn.style.opacity = "0";
        }
    });
}

function showFileName(input) {
    if (input.files && input.files[0]) {
        document.getElementById("image-name").innerText = input.files[0].name;
        document.getElementById("image-name").style.backgroundColor = "lightblue";
        document.getElementById("image-name").title = "Can choose another image";
    }
}

document.querySelectorAll(".status-list").forEach(td => {
    if (td.innerText.trim() === "Available" || td.innerText.trim() === "Active")
        td.style.color = "#36ed36";
    else
        td.style.color = "#c2180cff";
});

if (window.location.pathname.includes("/Menu/Insert/") || window.location.pathname.includes("/Customer/Insert/")) {
    let element = document.getElementById("nav-insert")
    resetMenuStyles(element)
} else {
    let element = document.getElementById("nav-display")
    resetMenuStyles(element)
}
function resetMenuStyles(element) {
    try {

        element.style.transform = "scale(1.1)";
        element.style.padding = "5px";
        element.style.color = "#ff9900";
        element.style.backgroundColor = "#1a19196e";
    }
    catch (error) {
        console.log("Error resetting menu styles:", error);
    }
}



// Define new flex-basis values for each column
const flexBasisValues = {
    'col-1': '8%',
    'col-2': '12%',
    'col-3': '25%',
    'col-4': '15%',
    'col-5': '12%',
    'col-6': '13%',
    'col-7': '8%'
};

console.log(window.location.pathname);
// Apply flex-basis directly to all elements with the class

if (window.location.pathname.includes("/Order/")) {
    for (const colClass in flexBasisValues) {
        const cols = document.querySelectorAll(`.${colClass}`);
        cols.forEach(col => {
            col.style.flexBasis = flexBasisValues[colClass];
            if (colClass === 'col-4') {
                const img = col.querySelector('img');
                if (img) {
                    img.style.borderRadius = "5px";
                    img.style.boxShadow = "1px 6px 5px 0px rgba(0,0,0,0.1)";
                }
            }
            console.log(`Set flex-basis of ${colClass} to ${flexBasisValues[colClass]}`);
        });
    }
}



try {
    if (document.querySelector('input[type="hidden"]').value === '1') {
        // Show the order form
        document.getElementById('create-order').style.display = 'block';
        console.log("Step 1: Show create order form");
    }
} catch (error) {
    console.log("Error showing create order form:", error);
}


try {
    document.querySelectorAll('.qincrement').forEach(button => {
    button.addEventListener('click', () => {
        let container = ''
        if (window.location.pathname.includes("/Order/Display/")){
            container = button.closest('tr');

        }
        else{
            container = button.closest('.table-row');
        }
        const quantityele = container.querySelector('.orquantity');
        const inputele = container.querySelector('.orquantity-result');
        let value = parseInt(quantityele.innerText);
            if (value < 100) {
                value++;
                quantityele.innerText = value;
                inputele.value = value;
                console.log(value);
            }
        });
    })
} catch (error) {
    console.log("Error incrementing quantity:", error);
}



try {
    document.querySelectorAll('.qdecrement').forEach(button => {
    button.addEventListener('click', () => {
        let container = ''
        if (window.location.pathname.includes("/Order/Display/")){
            container = button.closest('tr');

        }
        else{
            container = button.closest('.table-row');
        }
        const quantityele = container.querySelector('.orquantity');
        const inputele = container.querySelector('.orquantity-result');
        let value = parseInt(quantityele.innerText);
            if (value > 1) {
                value--;
                quantityele.innerText = value;
                inputele.value = value;
                console.log(value);
            }
        });
    })
} catch (error) {
    console.log("Error incrementing quantity:", error);
}


try {
    if (window.location.pathname.includes("/Customer/View/")) {
        document.querySelectorAll('li div form select').forEach(select => {
            if (select.value === "pending") {
                select.closest("li").querySelector('input[type="submit"]').style.backgroundColor = "orange";
            }
            if (select.value === "confirmed") {
                select.closest("li").querySelector('input[type="submit"]').style.backgroundColor = "blue";
            }
            if (select.value === "cancelled") {
                select.closest("li").querySelector('input[type="submit"]').style.backgroundColor = "red";
            }

        });
    }
} catch (error) {
    console.log("Error in try-catch block:", error);
}

try{
    console.log(document.getElementById("orcustname").value)
    console.log(document.getElementById("orcustphone").value)
    if (document.getElementById("orcustname").value != "")
        document.getElementById("step_step").value = "2"
    console.log(document.getElementById("step_step"))

}catch (error) {
    console.log("Error in try-catch block:", error);
}
