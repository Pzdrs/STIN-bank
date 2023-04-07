const input = document.querySelector('input[name=code]');
input.addEventListener('input', ev => {
    if (ev.target.value.length === 6) input.form.submit()
});