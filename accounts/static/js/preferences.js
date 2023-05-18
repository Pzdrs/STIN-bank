const twoFAStatus = document.querySelector('script#twoFA_status').innerText;
const twoFASwitch = document.querySelector('input#twoFA_switch');
twoFASwitch.checked = twoFAStatus === 'true';

function form_submit(checkbox) {
    document.querySelector('input#twoFAhidden').value = checkbox.checked;
    checkbox.form.submit();
}
