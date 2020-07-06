function handleEnter (field, event) 
{
	var keyCode = event.keyCode ? event.keyCode : event.which ? event.which : event.charCode;
	if (keyCode == 13) {
		var i;
		for (i = 0; i < field.form.elements.length; i++)
			if (field == field.form.elements[i])
				break;
		i = (i + 1) % field.form.elements.length;
		field.form.elements[i].focus();
		field.form.elements[i].select();
		return false;
	} else {
		return true;
	}
}


function mask(str,textbox,loc,delim) {
	var locs 	= loc.split(',');
	for (var i = 0; i <= locs.length; i++) {
		for (var k = 0; k <= str.length; k++) {
	 		if(k == locs[i]) {
	  			if(str.substring(k, k+1) != delim) {
	    			str = str.substring(0,k) + delim + str.substring(k,str.length)
	  			}
	 		}
		}
 	}
	textbox.value = str
}



function cekusia_baru(elem)
{
    var tenor
    var now=$('#id_tglpengajuan').val()
    var sekarang =  now.substr(6,4)
    var sekarangbulan =  now.substr(3,2)
    var harisekarang  =  now.substr(0,2)
    var tahunlahir = elem.substr(6,4)
    var bulanlahir = elem.substr(3,2)
    var harilahir = elem.substr(0,2)
    var usiana =  parseFloat(sekarang) - parseFloat(tahunlahir);
    var bulanusiana = parseFloat(sekarangbulan) - parseFloat(bulanlahir);
    var hariusiana = parseFloat(harisekarang) - parseFloat(harilahir);
    var min_usia = $('#min_usia').val();
    var max_usia = $('#max_usia').val();
    //
    var now = tahunlahir;
    var month = ("0" + bulanlahir).slice(-2);
    var day = ("0" + (harilahir)).slice(-2);

    var today = day +"-"+ (month)+"-"+ now ;
    if(usiana < min_usia ){
        //else if(&& bulanusiana <= 0 && hariusiana <= 0){)
            jAlert(usiana+' Thn Usia belum memenuhi syarat,Inputan Salah ');
            $('#tgllahir').val('');
            $('#thnusia').val('');
            $('#blnusia').val('');
            $('#hariusia').val('');
            $('#tgllahir').focus(); 

	//ganti dengan di database

    }else if(usiana > max_usia){
        jAlert(usiana+' Usia Melebihi dari ketentuan');
        $('#tgllahir').val('');
        $('#thnusia').val('');
        $('#blnusia').val('');
        $('#hariusia').val('');
        $('#tgllahir').focus();
    }else{
        if(hariusiana < 0){
            var hari = hariusiana+30
            var bulan = bulanusiana-1
            if(bulan < 0){
                var bulan=bulan+12
                var tahun = usiana-1
            }else{
                var bulan=bulan
                var tahun = usiana
            }
            $('#hariusia').val(hari);
            $('#blnusia').val(bulan);
            $('#thnusia').val(tahun);  
            $('#tanggal_lahir').val(today);  
        }else if(bulanusiana < 0){
            $('#hariusia').val(hariusiana);
            $('#blnusia').val(bulanusiana+12);
            $('#thnusia').val(usiana-1);    
            $('#tanggal_lahir').val(today);
        }else{
            $('#hariusia').val(hariusiana);
            $('#blnusia').val(bulanusiana);
            $('#thnusia').val(usiana);    
            $('#tanggal_lahir').val(today);
        }
        tenor_kosong();
        $('#produk').val('');

    }

}

function masker(str,textbox,loc,delim) {
    var locs    = loc.split(',');
    for (var i = 0; i <= locs.length; i++) {
        for (var k = 0; k <= str.length; k++) {
            if(k == locs[i]) {
                if(str.substring(k, k+1) != delim) {
                    str = str.substring(0,k) + delim + str.substring(k,str.length)
                }
            }
        }
    }
    textbox.value = str
}

function plafond()
{
    var gajiberish = $('#gajibersih').val(); 
    var persangs = $("#pers_max").val();
    plafon1 = 1*($('#tenor').val())*((persangs/100)*parseInt(MoneyToNumber(gajiberish)));
    plafon2 = 1 + (($('#flat_bln').val()/100) * ($('#tenor').val()));    
    plafon3 = Math.floor(plafon1 / plafon2);
    var tenor = $('#tenor').val();  
    if(plafon3 > 300000000){
        $('#plafonmax').val(currencyR(300000000));
    }else{
        $('#plafonmax').val(currencyR(plafon3));    
    }
}

