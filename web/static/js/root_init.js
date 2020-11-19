function checkRegistryData() {
    var data = new Array(2);
    data[0] = document.getElementsByName("first_password")[0].value;
    data[1] = document.getElementsByName("second_password")[0].value;

    var valid = true;
    if (data[0] == "" || data[1] == "" ){
        alert("Есть пустые поля. Попробуйте снова.");
        valid = false;
    }
    else if (data[0] != data[1]){
        alert("Пароли не совпадают. Попробуйте снова.");
        valid = false;
    }

    return valid;
}