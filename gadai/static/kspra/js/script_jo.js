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
    var now=$('#tglinput').val()
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
    if(usiana < min_usia ){
        //else if(&& bulanusiana <= 0 && hariusiana <= 0){)
            jAlert(usiana+' Usia belum memenuhi syarat ');
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
        }else if(bulanusiana < 0){
            $('#hariusia').val(hariusiana);
            $('#blnusia').val(bulanusiana+12);
            $('#thnusia').val(usiana-1);    
        }else{
            $('#hariusia').val(hariusiana);
            $('#blnusia').val(bulanusiana);
            $('#thnusia').val(usiana);    
        }
        tenor_kosong();
        $('#produk').val('');

    }

}




function cekusia(elem)

{
    var tenor
    var now=$('#tglinput').val()
    var sekarang =  now.substr(6,4)
    var sekarangbulan =  now.substr(3,2)
    var harisekarang  =  now.substr(0,2)
    var tahunlahir = elem.substr(6,4)
    var bulanlahir = elem.substr(3,2)
    var harilahir = elem.substr(0,2)
    var usiana =  parseFloat(sekarang) - parseFloat(tahunlahir);
    var bulanusiana = parseFloat(sekarangbulan) - parseFloat(bulanlahir);
    var hariusiana = parseFloat(harisekarang) - parseFloat(harilahir);
    if(usiana <= 39 ){
        //else if(&& bulanusiana <= 0 && hariusiana <= 0){)
            jAlert(usiana+' Usia belum memenuhi syarat ');
            $('#tgllahir').val('');
            $('#thnusia').val('');
            $('#blnusia').val('');
            $('#hariusia').val('');
            $('#tgllahir').focus(); 
    }else if(usiana > 74){
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
        }else if(bulanusiana < 0){
            $('#hariusia').val(hariusiana);
            $('#blnusia').val(bulanusiana+12);
            $('#thnusia').val(usiana-1);    
        }else{
            $('#hariusia').val(hariusiana);
            $('#blnusia').val(bulanusiana);
            $('#thnusia').val(usiana);    
        }
        var usianplusumur = Math.ceil((($('#thnusia').asNumber({parseType:'int'})*12)+$('#blnusia').asNumber({parseType:'int'}))/12)
        var usiammaxx = 75
        var jumusialunas 
        tenor = usiammaxx - $('#thnusia').val();
        if(tenor > 15){
            tenor =15
            jumusialunas =tenor+$('#thnusia').val();
        }else{
                tenor = tenor
                jumusialunas = tenor+$('#thnusia').asNumber({parseType:'int'});
        }
        if(jumusialunas==75 && $('#blnusia').val()==0 &&  $('#hariusia').val()==0){
            $('#tenormaks').val(tenor*12-$('#blnusia').val()-2);
        }else if(jumusialunas==75 && ($('#blnusia').val()!=0 || $('#hariusia').val()!=0)){
            $('#tenormaks').val(Math.floor((tenor-0.2)*12)-$('#blnusia').val());
        }else{
            $('#tenormaks').val(tenor*12);
        }
    }   

}




function FormatCurrency(objNum)

{ 

    var num = objNum.value

	var ent, dec;



	if (num != '' && num != objNum.oldvalue)

	{

		num = MoneyToNumber(num);

		if (isNaN(num))

		{ 

			objNum.value = (objNum.oldvalue)?objNum.oldvalue:'';

		} 

		else 

		{

			var ev = (navigator.appName.indexOf('Netscape') != -1)?Event:event;

			if (ev.keyCode == 190 || !isNaN(num.split('.')[1]))

			{ 

				alert(num.split('.')[1]);

							objNum.value = AddCommas(num.split('.')[0])+'.'+num.split('.')[1];

			}

			else

			{ 

				objNum.value = AddCommas(num.split('.')[0]);

			}

			objNum.oldvalue = objNum.value;

		}



	}

}



function MoneyToNumber(num)

{

	return (num.replace(/,/g, ''));

}



function AddCommas(num)

{

   numArr=new String(num).split('').reverse();

   for (i=3;i<numArr.length;i+=3)

    {

		numArr[i]+=',';

    }

    return numArr.reverse().join('');

}

function maks_angsuran()
{
    var net_p = parseFloat(to_number($("#gajibersih").val()))
    var dsr = parseFloat(to_number($("#pers_max").val())) / 100
    hitung = net_p * dsr
    return $("#angs_max").val(format_number(String(Math.round(hitung))));
}

function Biaya_Mutasi() {
    var mutasi = $('#mutasi').val()
    var e = document.getElementById('tonominal');
    if (mutasi==1) {
        e.value=currencyR(150000);
    }else{
		e.value=0;
	}

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
function cek_plafond()

{
    var plafondmax     = $('#plafonmax').val();
    var plafonusul     = $('#plafonusul').val();
    if(parseFloat((plafonusul).replace(/,/g, ''), 10) > parseFloat((plafondmax).replace(/,/g, ''), 10)){
        alert("Plafond Usul melebihi maksimal");
        $('#plafonusul').val('');
        return false;
    }   
}


function dsr()
{
	var kode_inst = $('#kode_inst').val();
	jenis = kode_inst.split(".")
	if(jenis[1]=='3'){
		//perubahan 95
		$('#pers_max').val('90')
	}else{
		$('#pers_max').val('90')

	}

}



function angsuran_kosong()
{
	$('#angsuran').val('');	
}

function plafonmask_kosong()
{
	$('#plafonmax').val('');	
    $('#plafonusul').val('');
	$('#angsuran').val('');
}

function persen_angsuran()
{
	var angsuran = $('#angsuran').val();	
	var maskang = $('#angs_max').val();
	var persen = parseFloat((angsuran).replace(/,/g, ''), 10)/parseFloat((maskang).replace(/,/g, ''), 10)
	$('#pers_angs').val(Math.round(persen*100))

}



function masker(str,textbox,loc,delim) {

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




