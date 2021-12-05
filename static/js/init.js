function alert_func(str = "") {
  alert("I am an alert box!" + str);
}

var x = document.getElementsByClassName('mdc-button');
var i;
for (i = 0; i < x.length; i++) {
  mdc.ripple.MDCRipple.attachTo(x[i]);
} 

x = document.getElementsByClassName('mdc-text-field');
for (i = 0; i < x.length; i++) {
  mdc.textField.MDCTextField.attachTo(x[i]);
}

x = document.getElementsByClassName('mdc-list-item');
for (i = 0; i < x.length; i++) {
  mdc.ripple.MDCRipple.attachTo(x[i]);
} 

const navList = new mdc.list.MDCList.attachTo(document.querySelector('.mdc-list'));
navList.wrapFocus = true;

const linearProgress = new mdc.linearProgress.MDCLinearProgress.attachTo(document.querySelector('.mdc-linear-progress'));
linearProgress.determinate = false;
linearProgress.close();

// init snack bars
var snack_bar_btn = mdc.snackbar.MDCSnackbar.attachTo(document.querySelector('#snackbar-btn'))
function show_snack_with_btn(content, btn_str) {
  document.querySelector("#snack-btn-content").innerHTML = content;
  document.querySelector("#snack-btn-btnlable").innerHTML = btn_str;
  snack_bar_btn.open();
}

var snack_bar_nobtn = mdc.snackbar.MDCSnackbar.attachTo(document.querySelector('#snackbar-nobtn'))
function show_snack_with_nobtn(content) {
  document.querySelector("#snack-nobtn-content").innerHTML = content;
  snack_bar_nobtn.open();
}

x = document.getElementsByClassName('mdc-ripple-surface');
for (i = 0; i < x.length; i++) {
  mdc.ripple.MDCRipple.attachTo(x[i]);
}

window.sr = ScrollReveal({ reset: false });
sr.reveal('#explore-content .mdc-card', { 
  origin: 'right', 
  duration: 1000 
});