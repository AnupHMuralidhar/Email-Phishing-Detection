function checkEmail(emailId) {
    fetch(`/email/${emailId}`, {
        method: 'GET',
    })
    .then(response => {
        if (response.redirected) {
            window.location.href = response.url;
        }
    });
}
