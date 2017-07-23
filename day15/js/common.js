/**
 * Created by Administrator on 2017/7/23.
 */
function GoTop(){
                document.body.scrollTop = 0;
            }

function ChangeMenu(nid){
    var current_header = document.getElementById(nid);

    var item_list = current_header.parentElement.parentElement.children;

    for(var i=0;i<item_list.length;i++){
        var current_item = item_list[i];
        current_item.children[1].classList.add('hide');
        current_item.children[1].parentElement.style.backgroundColor = "#2a3542";
        current_item.children[0].children[1].innerText = "+";
    }

    current_header.nextElementSibling.classList.remove('hide');
    current_header.parentElement.style.backgroundColor = "#35404d";
    current_header.children[1].innerText = "-";
}

function showModel() {
            document.getElementById("i1").classList.remove("hide");
            document.getElementById("i2").classList.remove("hide");
        }

function hideModel() {
    document.getElementById("i1").classList.add("hide");
    document.getElementById("i2").classList.add("hide");
}

function ChooseAll() {
    var tbody = document.getElementById("tb1");
    var tr_list = tbody.children;
    for(var i=0;i<tr_list.length;i++){
        var current_tr = tr_list[i];
        var checkbox = current_tr.children[0].children[0];
        checkbox.checked = true;
    }
}

function ReverseAll() {
    var tbody = document.getElementById("tb1");
    var tr_list = tbody.children;
    for(var i=0;i<tr_list.length;i++){
        var current_tr = tr_list[i];
        var checkbox = current_tr.children[0].children[0];
        if(checkbox.checked){
            checkbox.checked = false;
        }else{
            checkbox.checked = true;
        }
    }
}

function CancelAll() {
    var tbody = document.getElementById("tb1");
    var tr_list = tbody.children;
    for(var i=0;i<tr_list.length;i++){
        var current_tr = tr_list[i];
        var checkbox = current_tr.children[0].children[0];
        checkbox.checked = false;
    }
}