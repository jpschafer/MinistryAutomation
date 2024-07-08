// Scrapes a Verse of the Day From YouVersion's Web Page
// Necessary since there is not an RSS Feed or something cleaner like an API I can hit From 
// (I'm sure I could reverse-engineer theirs if I 'wanted', but that's a bit too much work, plus I think the web page is generated on the server-side).
// This unfortunately cannot run exclusively on Zapier due to requiring Puppeteer as a 3rd party dependency. Maybe there is a way you could minify and bundle your code
// to get away with a minified JS to shove in Zapier that has everything together, but I'm not sure how that would work or if a tool like that exists. 
// Normally things aren't run like that.

const fs = require("fs");
const fb = require("fb");
const cron = require("node-cron");
const puppeteer = require("puppeteer");
const { Command } = require("commander");
const program = new Command();

const BASE_URL = "https://www.bible.com";
const WEB_PAGE = BASE_URL + "/verse-of-the-day";

async function getVerse() {
	const browser = await puppeteer.launch();
	const page = await browser.newPage();
	await page.goto(WEB_PAGE);

    const imgSrc = await page.evaluate(() => {
        const srcs = Array.from(
        document.querySelectorAll("img.rounded-0\\.5.relative")
        ).map((image) => this.BASE_URL + image.getAttribute("src"));
        const cleanSrc = srcs[0].replace(/undefined\/_next\/image\?url=https%3A%2F%2Fimageproxy.youversionapi.com%2F\d*x\d*%2F/, "").replace(/&w=\d*&q=\d*/, "");
		const decodedSrc = decodeURIComponent(decodeURIComponent(cleanSrc));
		return decodedSrc;
    });

	const verse = await page.evaluate(() => {
        const srcs = Array.from(
        document.querySelectorAll("a.w-full.no-underline.text-text-light")
        ).map((a) =>  a.innerText);
        return srcs[0];
    });

	const verseRef = await page.evaluate(() => {
        const srcs = Array.from(
        document.querySelectorAll("p.dark\\:text-text-dark.font-aktiv-grotesk.uppercase.font-bold.mbs-2.text-gray-25")
        ).map((a) =>  a.innerText);
        return srcs[0];
    });

	const finalizedVerse = verse + " - " + verseRef;

	console.log("Verse we found", '[' + finalizedVerse +']');

	await browser.close();

    return {verseText: finalizedVerse, imgSrc: imgSrc};
};


async function getPages(key) {
    const pages = await fb.api('/v19.0/me/accounts',
    'GET',
    {access_token: key}).then(function (response) {
        if (response.error) {
        	console.error("Error:", response.error);
			return;
        }
		return response.data;
	}).catch(function(error) {
		if (error.error) {
        	console.error("Error:", response.error);
		} else {
			console.error("Unknown Error");
		}
	});
	return pages;
}

async function submitVerseToFacebook(key, verse) {
	let pages = await getPages(key);

	for (page of pages) {
		console.log("Page:", page);
		console.log(verse);
		console.log(verse.imgSrc);
		const response = await fb.api('/v19.0/' + page.id + '/photos',
			'POST',
			{access_token: page.access_token, caption: verse.verseText, url: verse.imgSrc},
			function (response) {
				if (response.error) {
					console.log(response.error);
				}
				console.log("Successfully submitted Photo to: " + page.name)
			});
	}
}
async function main(key, crontab) {
	console.log('crontab:', crontab);
	cron.schedule(crontab, async () => {
		const verse = await getVerse();
		await submitVerseToFacebook(key, verse)
	});
}

if (require.main === module) {
	program
		.version('1.0.0', '-v, --version')
		.usage('[OPTIONS]...')
		.requiredOption('-c, --crontab <value>', 'Cron Schedule to Post Verse of the Day On', '0 13 * * 3') // By Default do this as a Weekly Wednesday Thing @ 1pm
		.requiredOption('-k, --key <value>', 'System User Key To Pull Available Pages From')
		.parse(process.argv);

		const options = program.opts();
		
		if (options.key) {
			main(options.key, options.crontab);
		} else {
			console.log("need System User Key, exiting ...");
		}
	}
else {
	console.log("This was required as a module")
}