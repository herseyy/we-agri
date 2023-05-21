function check_token(){
	fetch("/")
		.then(response => response.json())
		.then(data => {
		console.log(data)
		if (data['detail']){
			window.location.href = '../login';
		}
		else {
			window.location.href = '../profile';
		}
		}).catch((error) => {
	      console.error('Error:', error);
	    });
}
