const input = document.querySelector('input[name=code]');
input.addEventListener('keydown', ev => {
    if (!/\d/.test(ev.key) && ev.key !== 'Backspace') {
        ev.preventDefault();
    }
});

input.addEventListener('input', ev => {
    ev.target.value = ev.target.value.replace(/\D/g, '');
    if (ev.target.value.length === 6) {
        input.form.submit();
    }
});