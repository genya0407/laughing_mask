<uploader>
	<h1>Upload</h1>

	<div>
		<input type='file' name='files[]' onchange='{handleSelectFiles}' multiple />
	</div>

	<div>
		<ul>
			<li each='{ imageDataURL in raw_image_data_urls }'>
				<img src='{ imageDataURL }' style='width: 500px;'/>
			</li>
		</ul>
		<ul>
			<li each='{ image in masked_images }'>
				<img src='data:image/png;base64,{ image }' style='width: 500px;' />
			</li>
		</ul>
	<div>

	const upload_url = 'https://2wm859rbjg.execute-api.us-west-2.amazonaws.com/dev/image';

	this.raw_image_data_urls = [];
	this.masked_images = [];

	Object.defineProperty(FileList.prototype, 'map', {
  		value: Array.prototype.map,
  		enumerable: false
	});

	Object.defineProperty(FileList.prototype, 'filter', {
  		value: Array.prototype.filter,
  		enumerable: false
	});

	handleSelectFiles(evt){
	    const files = evt.target.files;
	    const imageFiles = files.filter((file)=>{
	    	return file.type.match('image.*');
	    });

	    Promise.all(imageFiles.map((file)=>{
	    	return new Promise((resolve)=>{
		    	var fileReader = new FileReader();
		    	fileReader.onload = function(e){
	    			resolve(e.target.result);
	    		};
	    		fileReader.readAsDataURL(file);
	    	});
	    })).then((image_data_urls)=>{
	    	this.raw_image_data_urls = image_data_urls;
	    	this.update();
	    });

	    const maskedImagePromises = imageFiles.map((file)=>{
	    	return new Promise((resolve)=>{
	    		var fileReader = new FileReader();
	    		fileReader.onload = function(e){
	    			const b64encoded = btoa(e.target.result);
	    			resolve(b64encoded);
	    		};
	    		fileReader.readAsBinaryString(file);
	    	}).then((b64encoded)=>{
	    		return axios.post(upload_url, {
	    			image: b64encoded
	    		});
	    	}).then((response)=>{
	    		return new Promise((resolve)=>{
	    			resolve(response.data.image);
	    		});
	    	});
	    });

	    Promise.all(maskedImagePromises).then((images)=>{
			this.masked_images = images;
			this.update();
	    });
    }
</uploader>