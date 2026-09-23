const links = document.querySelectorAll(".menu a");

links.forEach((link) => {

    link.addEventListener("click", () => {

        links.forEach((item) => {
            item.classList.remove("ativo");
        });

        link.classList.add("ativo");

    });

});