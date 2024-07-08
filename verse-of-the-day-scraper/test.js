const puppeteer = require("puppeteer");
const fs = require("fs");

const WEB_PAGE = "https://www.bible.com/verse-of-the-day";

(async () => {
	const browser = await puppeteer.launch();
	const page = await browser.newPage();
	await page.goto(WEB_PAGE);
	await page.screenshot({ path: "example.png" });

    const imgSrc = await page.evaluate(() => {
        const srcs = Array.from(
        document.querySelectorAll("img.rounded-0\\.5.relative")
        ).map((image) => "https://www.bible.com" + image.getAttribute("src"));
        return srcs[0];
    });
	// Persist data into data.json file
	fs.writeFileSync("./data.json", JSON.stringify(imgSrc));
	console.log("File is created!");
	await browser.close();
})();