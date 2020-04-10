const franc = require('franc');
const fs = require('fs');
const { parse } = require('json2csv');

function getData() {
	return new Promise((resolve, reject) => {
		const text = fs.readFileSync('../Dataset/x_new_test.txt', (encoding = 'utf-8')).split('\n');
		const text_train = fs.readFileSync('../Dataset/x_new_train.txt', (encoding = 'utf-8')).split('\n');
		text.push(...text_train);

		// text_series = new Series(text)

		const labels = fs.readFileSync('../Dataset/y_new_test.txt', (encoding = 'utf-8')).split('\n');
		const labels_train = fs.readFileSync('../Dataset/y_new_train.txt', (encoding = 'utf-8')).split('\n');
		labels.push(...labels_train);

		// label_series = new Series(labels)

		resolve([text, labels]);
	});
}

function getCombinedData() {
	return new Promise((resolve, reject) => {
		const text = fs.readFileSync('../output/new_data/combined_text_40.txt', (encoding = 'utf-8')).split('\n');
		// text_series = new Series(text)

		const labels = fs.readFileSync('../output/new_data/combined_labels_40.txt', (encoding = 'utf-8')).split('\n');

		// label_series = new Series(labels)

		resolve([text, labels]);
	});
}

function predictSingleLanguage(text, label) {
	return new Promise((resolve, reject) => {
		const startTime = Date.now();
		const prediction = franc(text);
		const endTime = Date.now();

		if (prediction === label) {
			resolve([true, (endTime - startTime) / 1000]);
		}
		resolve([false, (endTime - startTime) / 1000]);
	});
}

function predictMultipleLanguages(text, label) {
	return new Promise((resolve, reject) => {
		let score = 0;
		const startTime = Date.now();
		const prediction = franc.all(text, { only: ['eng', 'slk', 'fra', 'slv', 'ita', 'deu', 'spa', 'nld'] });
		const endTime = Date.now();

		const lang1 = label.slice(2, 5),
            lang2 = label.slice(9, 12);
		
		if(prediction[0][0] == "und"){
			resolve([score, ((endTime - startTime) / 1000)]);	
		}
		if (prediction[0][0] === lang1 || prediction[0][0]=== lang2) {
            score += 1;
		}
		if (prediction[1][0] === lang1 || prediction[1][0]=== lang2) {
            score += 1;
		}
		if (prediction[0][0] === lang1) {
            score += 2;
		}
		if ((prediction[0][0] === lang1) && (prediction[1][0] === lang2)) {
            score += 3;
        }

		resolve([score, ((endTime - startTime) / 1000)]);
	});
}

async function runTest(mode, input_file, texts, labels) {
	let file;

	try {
		file = fs.openSync(input_file, 'a');
		let data = parse([{ franc: 'franc', time: 'time' }], { header: false });
		for (let i = 0; i < texts.length; i++) {
			if (i % 1000 === 0) {
				console.log('Predicted on %d texts', i);
			} 
			let prediction, time;
			if (mode === 'single') {
				[prediction, time] = await predictSingleLanguage(texts[i], labels[i]);
			} else if (mode === 'combined') {
				[prediction, time] = await predictMultipleLanguages(texts[i], labels[i]);
			}

			data = parse([{ franc: prediction, time: time }], { header: false });
			fs.appendFileSync(file, '\n' + data, 'utf-8');
		}
	} catch (error) {
		console.log(error);
	} finally {
		if (file !== undefined) {
			fs.closeSync(file);
		}
	}
}

// getData().then(([texts,labels])=>{
//     runTest('single','./output/franc_results_single.csv',texts,labels)
// }).catch((error)=>{console.log('Error occured. Reason:',error.message)});

getCombinedData()
	.then(([texts, labels]) => {
		runTest('combined', './output/franc_results_multiple_40.csv', texts, labels);
	})
	.catch((error) => {
		console.log('Error occured. Reason:', error.message);
	});
