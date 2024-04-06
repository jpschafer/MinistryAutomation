// Scrapes a Verse of the Day From YouVersion's Web Page
// Necessary since there is not an RSS Feed or something cleaner like an API I can hit From 
// (I'm sure I could reverse-engineer theirs if I 'wanted', but that's a bit too much work, plus I think the web page is generated on the server-side).
// This unfortunately cannot run exclusively on Zapier due to requiring Puppeteer as a 3rd party dependency. Maybe there is a way you could minify and bundle your code
// to get away with a minified JS to shove in Zapier that has everything together, but I'm not sure how that would work or if a tool like that exists. 
// Normally things aren't run like that.

