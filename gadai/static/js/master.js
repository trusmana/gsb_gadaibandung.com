function format_number(num) {
    num = parseFloat(num).toFixed(2)
    var sre = new RegExp('([0-9]+)([0-9]{3})');
    var frac = String(num).split('.')[1];
    var decimal = String(num).split('.')[0];
    var ret_num = decimal + '';
    while (sre.test(ret_num)) { ret_num = ret_num.replace(sre, '$1' + '.' + '$2')}
    if ((frac == undefined) || (frac == '00')) { return ret_num; }
    else { return ret_num + ',' + frac; }
}

function to_number(str) {
    return parseFloat(str.replace(/\./g, '').replace(/,/g, '.'));
}

