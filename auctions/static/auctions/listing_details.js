document.addEventListener('DOMContentLoaded', function () {

    const modal = document.querySelector('.modal');

    if (modal.classList.contains('hasError')) {
        const myModal = new bootstrap.Modal(document.getElementById('exampleModal'));
        myModal.show();
    }
});