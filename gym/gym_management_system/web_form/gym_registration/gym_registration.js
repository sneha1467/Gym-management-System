// frappe.ready(function() {
// 	// bind events here
// })


frappe.ready(() => {
 if (frappe.web_form) {
 frappe.web_form.after_save = function () {
 window.location.href = 'http://127.0.0.1:8001/GYM';
};
}
});