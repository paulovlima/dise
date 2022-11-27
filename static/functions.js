function expandir() {
    var moreServ = document.getElementById('mais');
    var textobotao = document.getElementById('expandBtn');
    if (moreServ.style.display === 'none'){
        textobotao.innerHTML = 'Reduzir';
        moreServ.style.display = 'inline';
    } else {
        textobotao.innerHTML = 'Expandir';
        moreServ.style.display = 'none';
    }
}