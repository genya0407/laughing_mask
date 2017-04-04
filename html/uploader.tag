<uploader>
	<h1>Laughing man</h1>

	<input type='file' onchange='{handleSelectFiles}'/>
	<div id='image-canvas'>
		<img src='{image}' />
		<div class='{loader_class}' display='none' />
	</div>

	<script>
		const upload_url = 'https://2wm859rbjg.execute-api.us-west-2.amazonaws.com/dev/image';

		this.image = './no_data.jpg';
		this.loader_class = '';

		handleSelectFiles(evt){
		    const file = evt.target.files[0];

		    console.log(file.type)

		    if (!file.type.match('image/png') && !file.type.match('image/jpeg')) {
		    	alert('PNG or JPG only.');
		    	return;
		    }

	    	const fileReader = new FileReader();
	    	fileReader.onload = (e)=>{
				this.image = e.target.result;
				this.update()
			};
			fileReader.readAsDataURL(file);

	    	Promise.resolve(new Promise((resolve)=>{
	    		const fileReader = new FileReader();
	    		fileReader.onload = function(e){
	    			const b64encoded = btoa(e.target.result);
	    			resolve(b64encoded);
	    		};
	    		fileReader.readAsBinaryString(file);
	    	}).then((b64encoded)=>{
	    		this.loader_class = 'loader';
	    		this.update();
	    		return axios.post(upload_url, {
	    			image: b64encoded
	    		});
	    	}).then((response)=>{
				this.image = 'data:image/png;base64,' + response.data.image;
				this.loader_class = '';
				this.update();
		    }));
	    }
    </script>

    <style>
    	uploader {
    		width: 100%;
    		margin: 0px, auto, 0px, auto;
    	}

    	div#image-canvas {
    		position: relative;
    		margin-top: 10px;
    		width: 100%;
	    }

	    img {
	    	width: 500px;
	    }

		div.loader {
			position: absolute;
			z-index: 100;
			top: 100px;
			left: 174px;
			border: 16px solid #f3f3f3; /* Light grey */
			border-top: 16px solid #3498db; /* Blue */
			border-radius: 50%;
			width: 120px;
			height: 120px;
			animation: spin 2s linear infinite;
		}

		@keyframes spin {
			0% { transform: rotate(0deg); }
			100% { transform: rotate(360deg); }
		}
    </style>
</uploader>