function date_to_label(date){
	return `${date.getMonth()+1>9?date.getMonth()+1:'0'+(date.getMonth()+1)}.${date.getDate()>9?date.getDate():'0'+date.getDate()}`;
}
let majax = {
	post:function (url, data, success, error){
		$.ajax({
            url: url,
            type: 'post',
            dataType: 'json',
            contentType: 'application/json',
            success: function (res) { 
				if (success) success(res) 
			},
			error:function(res){ 
				if (error) error(res) 
			},
            data: JSON.stringify(data)
        });
	},
	get: function(url, data, success, error){
		$.ajax({
            url: url,
            type: 'get',
			data: data,
            success: function (res) { 
				if (success) success(res) 
			},
			error:function(res){ 
				if (error) error(res) 
			}
        });
	}

}
let user_auth = {
	login : function(){
		majax.post(
			"/api/user/login",
			{
				login: $('#auth_login').val(),
				password: $('#auth_password').val()
			},
			()=>{
				location.reload();
			},
			(ret)=>{
				alert(ret.responseJSON.detail);
			}
		)
	},
	logout :function(){
		majax.get("/api/user/logout",{}, ()=>{ location.reload(); })
	}
}
let user_data = {
	set_base_currency:function(){
		majax.post(
			"/api/user/set_base_currency",
			{ code: $('#base_currency').val() }
		)
	},
}
let wallets = {
	init:function(){
		this.wallets_chart=new Chart("wallets_chart", {
			type: "doughnut",
			data: {
				labels: [],
				datasets: []
			},
			options: { },
		})
		this.get_data();
	},
	data:{},
	total_base_value:0,
	get_data:function(){
		majax.get(
			'/api/personal_stat/wallets',
			{},
			(ret)=>{
				this.total_base_value = 0
				ret.forEach((row)=>{
					this.data[row.id]=row;
					this.total_base_value +=row.base_value;
				})
				this.draw_lines();
			}
		)
	},
	draw_lines :function(){
		$('#wallets_list').html('')
		for (id in this.data){
			let w = this.data[id]
			$('#wallets_list').append(`
				<div>${w.currency_code}</div>
				<div>${w.name}</div>
				<div>${w.value}</div>
				<div>${w.base_value}</div>
				<div><input class="add_cash_to_wallet" data-id="${w.id}"></div>
				<div><button onclick="wallets.add_cash(${w.id})">add</button></div>
				<div><button onclick="wallets.del(${w.id})">del</button></div>
			`)
		} 
		$('.wallets_list #total_base_value').html(this.total_base_value);
		this.draw_chart();
	},
	draw_chart: function(){
		let labels = [];
		let datasets = [{ data: [] }]
		for (id in this.data){
			let w = this.data[id];
			labels.push(`${w.currency_code} ${w.name}`)
			datasets[0].data.push(w.base_value)
		}
		this.wallets_chart.data.datasets = datasets;
		this.wallets_chart.data.labels = labels;
		this.wallets_chart.update();
	},
	add:function(){
		majax.post(
			'/api/personal_stat/add_wallet',
			{
				"currency_code": $('#add_wallet [name=code]').val(),
				"name": $('#add_wallet [name=name]').val()
			},
			()=>{
				this.get_data();
			}
		)
	},
	add_cash: function(wallet_id){
		majax.post(
			'/api/personal_stat/add_cash_to_wallet',
			{
				"wallet_id": wallet_id,
				"value": $(`.add_cash_to_wallet[data-id=${wallet_id}]`).val()
			},
			()=>{
				this.get_data();
			}
		)
	},
	del:function(wallet_id){
		if (!confirm('are you shure?')) return;
		majax.post(
			'/api/personal_stat/del_wallet',
			{
				"wallet_id": wallet_id
			},
			()=>{
				this.get_data();
			}
		)
	}
}
let currency_history = {
	init:function(){
		this.currency_history=new Chart("currency_history", {
			type: "line",
			data: {
				labels: [1,2,3,4],
				datasets: []
			},
			options: { },
		})
		this.get_data();
	},
	get_data: function(){
		majax.get(
			'/api/general_stat/currency_history',
			{
				base_currency:$('#base_currency').val()
			},
			(ret)=>{
				this.data = ret
				this.update()
			})
	},
	update: function(data){
		let min_date = new Date();
		let max_date = new Date();
		datasets = [];
		let show_currencies = $('#currencies').val();
		let base_currency = $('#base_currency').val();
		this.data.forEach((el)=>{
			if ( el.history && el.code !=base_currency && show_currencies.indexOf( el.code )+1 ){
				let points = []
				el.history.forEach((h)=>{
					let date = new Date(h.date)
					points.push({
						x:date_to_label(date),
						y:h.value
					})
					if ( min_date>date ) min_date=date;
					if ( max_date<date ) max_date=date;
				})
				datasets.push({
					label: el.code,
					pointRadius: 4,
					data: points,
					cubicInterpolationMode: 'monotone',
				})
			} 
		})
		let labels = []
		for (let date = min_date; date<=max_date; date.setDate(date.getDate() + 1) ){
			labels.push(date_to_label(date))
		} 
		this.currency_history.data.datasets = datasets;
		this.currency_history.data.labels = labels;
		this.currency_history.update();
	}
}
window.onload = () => {
	currency_history.init();
	$('#currencies').on('change',()=>{
		currency_history.update();
	})
	$('#base_currency').on('change',()=>{
		currency_history.get_data();
	})

	if ($('#login')[0]){
		$('#base_currency').on('change',()=>{
			user_data.set_base_currency();
		})
		wallets.init()
	}
};